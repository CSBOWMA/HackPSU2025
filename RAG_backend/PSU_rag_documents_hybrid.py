import json
import os

import azure.identity
import openai
from dotenv import load_dotenv
from lunr import lunr
from sentence_transformers import CrossEncoder
from langchain_community.vectorstores import FAISS 
from langchain_openai import OpenAIEmbeddings 



load_dotenv(override=True)



# Embedding client (OpenAI - for embeddings)
embedding_client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
EMBEDDING_MODEL = "text-embedding-3-small"
SYSTEM_MESSAGE = """
    You are a helpful course assistant for IA651: Machine Learning at Clarkson University.
    Your role is to help students with:
    - Course logistics (schedules, deadlines, policies)
    - Concept explanations (using lecture materials)
    - General course questions

    IMPORTANT GUIDELINES:
    1. Only use information from the provided course materials
    2. Always cite sources in square brackets [like this]
    3. If information is not in sources, say "I don't have this information in the course materials"
    4. Be supportive and educational
    5. Never provide direct solutions to active assignments
    """
# Generation client (Gemini via OpenRouter - for responses)
generation_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)
GENERATION_MODEL = os.getenv("GEMINI_MODEL", "google/gemini-2.0-flash-exp")

# Load documents and create index
documents = None
documents_by_id = None
index = None # LUNR Index (Full-Text)
FAISS_STORE = None # FAISS Index (Vector)


# --- UTILITY FUNCTION ---
def get_all_documents_from_faiss(faiss_path, embedding_client):
    """Loads all documents from a FAISS index and returns them as a list of dictionaries."""
    
    faiss_index = FAISS.load_local(
        faiss_path, 
        embedding_client, 
        allow_dangerous_deserialization=True
    )
    # The documents are not easily retrieved from FAISS as a full list.
    # We return the FAISS object itself for vector search.
    return faiss_index

def initialize_rag_faiss():
    """Initializes the FAISS vector store for vector search."""
    global FAISS_STORE
    
    # 1. Load Embedding Client (Necessary to load FAISS)
    embedding_client_loader = OpenAIEmbeddings(
        openai_api_key=os.environ["OPENAI_KEY"],
        model=EMBEDDING_MODEL
    )
    
    FAISS_PATH = "faiss_index_hackpsu"
    
    # Load the FAISS object
    FAISS_STORE = get_all_documents_from_faiss(FAISS_PATH, embedding_client_loader)
    print("FAISS Index loaded.")



def initialize_rag_lunr():
    """
    Loads all document content from FAISS for Lunr and dictionary lookups.
    """
    global documents, documents_by_id, index
    
    if FAISS_STORE is None:
        raise RuntimeError("FAISS Store must be initialized first. Run initialize_rag_faiss().")

    # This step retrieves ALL chunks from the FAISS object
    all_docs_raw = FAISS_STORE.docstore._dict.values()
    
    # Convert LangChain Documents back to your required dictionary structure
    document_list = []
    for i, doc in enumerate(all_docs_raw):
        # We manually re-create the structure that your old script expected
        # Use metadata source and a simple index ID
        chunk_id = f"{doc.metadata.get('source', 'unknown')}-{i + 1}"
        document_list.append({
            "id": chunk_id, 
            "text": doc.page_content,
            "metadata": doc.metadata,
        })
    
    documents = document_list
    documents_by_id = {doc["id"]: doc for doc in documents}
    
    # Build the full-text LUNR index with all the new data
    index = lunr(ref="id", fields=["text"], documents=documents)
    print("LUNR Index and document lookup tables built.")

def initialize_rag():
    """Unified initialization call."""
    initialize_rag_faiss()
    initialize_rag_lunr()
def full_text_search(query, limit):
    """
    Perform a full-text search on the indexed documents (LUNR).
    """
    if index is None:
        return []
    results = index.search(query)
    # Ensure the retrieved documents exist in the dictionary
    retrieved_documents = []
    for result in results:
        if result["ref"] in documents_by_id:
            retrieved_documents.append(documents_by_id[result["ref"]])
    return retrieved_documents[:limit]


def vector_search(query, limit):
    """
    Perform a vector search using the loaded FAISS index (LangChain method).
    This replaces your custom cosine similarity function which is no longer needed.
    """
    if FAISS_STORE is None:
        return []
        
    # We must create a temporary embedding client *inside* this function 
    # because the FAISS store needs a client with the same embeddings model for the query.
    # Note: This means every vector search hits the API.
    query_embedding_client = OpenAIEmbeddings(
        openai_api_key=os.environ["OPENAI_KEY"],
        model=EMBEDDING_MODEL
    )
    
    # Perform the search using FAISS's built-in similarity search
    # This returns LangChain Document objects
    lc_docs = FAISS_STORE.similarity_search(
        query, 
        k=limit,
        # The embedding model must be passed explicitly for the query calculation
        embeddings=query_embedding_client 
    )
    
    # Convert the returned LangChain Documents back to your required dictionary structure
    retrieved_documents = []
    for i, doc in enumerate(lc_docs):
        # Retrieve the document ID from the lookup table for consistency
        chunk_id = f"{doc.metadata.get('source', 'unknown')}-{i + 1}"
        retrieved_documents.append({
            "id": chunk_id,
            "text": doc.page_content,
            "metadata": doc.metadata,
        })
        
    return retrieved_documents


def reciprocal_rank_fusion(text_results, vector_results, k=60):
    """
    Perform Reciprocal Rank Fusion (RRF) on the results from text and vector searches.
    """
    scores = {}

    # Fusion for text results
    for i, doc in enumerate(text_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
        
    # Fusion for vector results
    for i, doc in enumerate(vector_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
        
    scored_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Ensure we only return IDs that exist in the documents_by_id map
    retrieved_documents = []
    for doc_id, _ in scored_documents:
        if doc_id in documents_by_id:
             retrieved_documents.append(documents_by_id[doc_id])
    
    return retrieved_documents


def rerank(query, retrieved_documents):
    """
    Rerank the results using a cross-encoder model.
    """
    # ... (Your existing rerank logic, assuming CrossEncoder is available) ...
    # Placeholder for the Reranker logic
    if not retrieved_documents:
        return []
    encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    scores = encoder.predict([(query, doc["text"]) for doc in retrieved_documents])
    # Combine scores with documents and sort
    scored_documents = [v for _, v in sorted(zip(scores, retrieved_documents), reverse=True)]
    return scored_documents


def hybrid_search(query, limit):
    """
    Perform a hybrid search using both full-text and vector search, then RRF and rerank.
    """
    # NOTE: We double the limit for the initial searches to ensure a high quality pool
    search_limit = limit * 3
    text_results = full_text_search(query, search_limit)
    vector_results = vector_search(query, search_limit)
    fused_results = reciprocal_rank_fusion(text_results, vector_results)
    reranked_results = rerank(query, fused_results)
    return reranked_results[:limit]


def answer_question(user_question):
    # ... (Your existing answer_question logic using the global GENERATION_CLIENT) ...
    SYSTEM_MESSAGE = """
    You are a helpful course assistant for IA651: Machine Learning at Clarkson University.
    Your role is to help students with:
    - Course logistics (schedules, deadlines, policies)
    - Concept explanations (using lecture materials)
    - General course questions

    IMPORTANT GUIDELINES:
    1. Only use information from the provided course materials
    2. Always cite sources in square brackets [like this]
    3. If information is not in sources, say "I don't have this information in the course materials"
    4. Be supportive and educational
    5. Never provide direct solutions to active assignments
    """
    print("Searching course materials...")
    retrieved_documents = hybrid_search(user_question, limit=5)

    if not retrieved_documents:
        print("No relevant documents found")
        return {
            "question": user_question,
            "answer": "I couldn't find relevant information in the course materials.",
            "sources": [],
            "guardrail_triggered": False
        }
    print(f"✓ Retrieved {len(retrieved_documents)} matching documents")
    context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])
        
    response = generation_client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": f"{user_question}\nSources: {context}"},
        ],
    )
        
    answer = response.choices[0].message.content
    sources = [doc["id"] for doc in retrieved_documents]
    return {
        "question": user_question,
        "answer": answer,
        "sources": sources,
    }

if __name__ == "__main__":
    initialize_rag()
    # Test the fix for the semantic gap
    print("--- Testing Semantic Gap Fix ---")
    result = answer_question("TA contact?")
    print(f"\nAnswer: {result['answer']}")
    print(f"Sources: {result['sources']}")
'''

def initialize_rag():
    """
    Load documents from JSON and create the search index.
    Must be called before any search operations.
    """
    global documents, documents_by_id, index
    
    with open("PSU_rag_ingested_chunks.json") as file:
        documents = json.load(file)
        documents_by_id = {doc["id"]: doc for doc in documents}
    
    index = lunr(ref="id", fields=["text"], documents=documents)
    
    # print(f"Loaded {len(documents)} document chunks")
    # print(f"Generation: Gemini via OpenRouter ({GENERATION_MODEL})")
    # print(f"Embeddings: OpenAI ({EMBEDDING_MODEL})\n")

def vector_search(query, limit):
    """
    Perform a vector search on the indexed documents
    using a simple cosine similarity function.
    """

    def cosine_similarity(a, b):
        return sum(x * y for x, y in zip(a, b)) / ((sum(x * x for x in a) ** 0.5) * (sum(y * y for y in b) ** 0.5))

    query_embedding = embedding_client.embeddings.create(model=EMBEDDING_MODEL, input=query).data[0].embedding
    similarities = []
    for doc in documents:
        doc_embedding = doc["embedding"]
        similarity = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((doc, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    retrieved_documents = [doc for doc, _ in similarities[:limit]]
    return retrieved_documents


def reciprocal_rank_fusion(text_results, vector_results, k=60):
    """
    Perform Reciprocal Rank Fusion (RRF) on the results from text and vector searches,
    based on algorithm described here:
    https://learn.microsoft.com/azure/search/hybrid-search-ranking#how-rrf-ranking-works
    """
    scores = {}

    for i, doc in enumerate(text_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
    for i, doc in enumerate(vector_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
    scored_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    retrieved_documents = [documents_by_id[doc_id] for doc_id, _ in scored_documents]
    return retrieved_documents


def rerank(query, retrieved_documents):
    """
    Rerank the results using a cross-encoder model.
    """
    if not retrieved_documents:
        return []
    encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    scores = encoder.predict([(query, doc["text"]) for doc in retrieved_documents])
    scored_documents = [v for _, v in sorted(zip(scores, retrieved_documents), reverse=True)]
    return scored_documents


def hybrid_search(query, limit):
    """
    Perform a hybrid search using both full-text and vector search.
    """
    text_results = full_text_search(query, limit * 2)
    vector_results = vector_search(query, limit * 2)
    fused_results = reciprocal_rank_fusion(text_results, vector_results)
    reranked_results = rerank(query, fused_results)
    return reranked_results[:limit]
def answer_question(user_question):
    SYSTEM_MESSAGE = """
    You are a helpful course assistant for IA651: Machine Learning at Clarkson University.
    Your role is to help students with:
    - Course logistics (schedules, deadlines, policies)
    - Concept explanations (using lecture materials)
    - General course questions

    IMPORTANT GUIDELINES:
    1. Only use information from the provided course materials
    2. Always cite sources in square brackets [like this]
    3. If information is not in sources, say "I don't have this information in the course materials"
    4. Be supportive and educational
    5. Never provide direct solutions to active assignments
    """
    print("Searching course materials...")
    retrieved_documents = hybrid_search(user_question, limit=5)

    if not retrieved_documents:
        print("No relevant documents found")
        return {
            "question": user_question,
            "answer": "I couldn't find relevant information in the course materials.",
            "sources": [],
            "guardrail_triggered": False
        }
    print(f"✓ Retrieved {len(retrieved_documents)} matching documents")
    context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])
        
    response = generation_client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": f"{user_question}\nSources: {context}"},
        ],
    )
    
    answer = response.choices[0].message.content
    sources = [doc["id"] for doc in retrieved_documents]
    return {
        "question": user_question,
        "answer": answer,
        "sources": sources,
    }

if __name__ == "__main__":
    initialize_rag()
    # user_question = "What are the key topics covered in the IA651 course syllabus?"
    # user_question = "Who is the TA?"
    user_question="Tell me about Taj Mahal in India"
    result = answer_question(user_question)
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")

        '''