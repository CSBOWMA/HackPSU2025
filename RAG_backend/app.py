import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from fastapi import BackgroundTasks # Optional, but good practice
import json
import PSU_rag_documents_hybrid as hybrid_retriever  # Import to ensure RAG components are available
from PSU_rag_documents_hybrid import  initialize_rag, hybrid_search, generation_client


# --- LangChain Imports ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# from langchain.retrievers import EnsembleRetriever # 🌟 NEW IMPORT for combining search methods
from langchain_community.retrievers import BM25Retriever # 🌟 NEW IMPORT for keyword search
from langchain_community.document_loaders import TextLoader # Needed for BM25 (or another loader if you use a full file)

load_dotenv()
app = FastAPI(title="HackPSU RAG API")
# Global variable to store the RAG Chain and Retriever (loaded once)
RAG_CHAIN = None
RETRIEVER = None

class QueryRequest(BaseModel):
    """Schema for the incoming user question."""
    question: str

class RAGResponse(BaseModel):
    """Schema for the outgoing RAG answer."""
    answer: str
    sources: list[str] = [] # List of unique source files

'''
def stream_rag_answer(query: str, retriever, rag_chain):
    """Retrieves and streams the LLM response."""
    sources = retriever.invoke(query)
    unique_sources = sorted(list(set(d.metadata.get('source') for d in sources)))
    yield f"{{'sources': {json.dumps(unique_sources)}}}" + "[METADATA_END]"

    # 3. Stream the LLM Answer
    for chunk in rag_chain.stream(query):
        # LangChain stream yields the final string chunk by chunk
        yield chunk
'''
def stream_rag_answer(query: str):
    """
    Performs the custom hybrid search and streams the LLM response.
    This replaces the LangChain chain.
    """
    
    # 1. CUSTOM HYBRID RETRIEVAL
    # Use your high-quality hybrid search function directly
    
    try:
        retrieved_documents = hybrid_search(query, limit=5)
        if not retrieved_documents:
            yield f"{{'sources': []}} [METADATA_END] I couldn't find any relevant information in the course materials for your query."
            return
        context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])
        unique_sources = sorted(list(set(doc["metadata"]["source"] for doc in retrieved_documents)))
        response_stream = generation_client.chat.completions.create(
            model=hybrid_retriever.GENERATION_MODEL,
            temperature=0.3,
            messages=[
                {"role": "system", "content": hybrid_retriever.SYSTEM_MESSAGE},
                {"role": "user", "content": f"{query}\nSources: {context}"},
            ],
            stream=True, # Enable streaming!
        )
        yield f"{{'sources': {json.dumps(unique_sources)}}}" + "[METADATA_END]"

        # Yield the answer chunks
        for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        yield f"{{'sources': []}} [METADATA_END] Error processing your query: {str(e)}"

@app.on_event("startup")
def load_rag_components():
    """Initializes the custom RAG logic and models into memory."""
    global RAG_CHAIN
    
    try:
        # Load all documents, create LUNR index, and initialize the models
        initialize_rag()
        print(f"Hybrid RAG Logic and Indexes loaded successfully! Model: {hybrid_retriever.GENERATION_MODEL}")
        if hybrid_retriever.index:
            doc_count = len(hybrid_retriever.documents) if hybrid_retriever.documents else 0
            print(f"✓ Hybrid RAG initialized successfully!")
            print(f"  - FAISS Vector Index: Ready")
            print(f"  - LUNR Full-Text Index: Ready ({doc_count} documents)")
            print(f"  - Generation Model: {hybrid_retriever.GENERATION_MODEL}")
            print(f"  - Supported Sources: PDF, IPYNB, CSV")
        else:
            print("⚠ Warning: RAG index not initialized properly")
    except Exception as e:
        print(f"FATAL ERROR during RAG initialization: {e}")
        # In a real app, you might crash the app, but here, log the error.

          
'''
# uncomment if you want Simple Vector search/ no-hybrid search
@app.on_event("startup")
def load_rag_components():
    """Initializes the FAISS index, LLM, and RAG chain into memory."""
    global RAG_CHAIN
    global RETRIEVER
    
    try:
        # Configuration
        OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
        OPENAI_KEY = os.environ["OPENAI_KEY"]
        EMBEDDING_MODEL = "text-embedding-3-small"
        GENERATION_MODEL = os.getenv("GEMINI_MODEL", "google/gemini-2.5-flash")

        print("--- Loading RAG Components ---")
        
        # A. Load Embeddings Client (to load the FAISS index)
        embedding_client = OpenAIEmbeddings(
            openai_api_key=OPENAI_KEY,
            model=EMBEDDING_MODEL
        )

        # B. Load Vector Store and Retriever
        vectorstore = FAISS.load_local(
            "faiss_index_hackpsu", 
            embedding_client, 
            allow_dangerous_deserialization=True
        )
        RETRIEVER = vectorstore.as_retriever(search_kwargs={"k": 5})

        # C. Load Generative Model (Gemini via OpenRouter)
        llm = ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=OPENROUTER_API_KEY,
            model=GENERATION_MODEL
        )

        # D. Define the RAG Prompt (your custom guardrail template)
        template = """
        You are a helpful course assistant for IA651: Machine Learning at Clarkson University.
        Your role is to help students with:
        - Course logistics (schedules, deadlines, policies)
        - Concept explanations (using lecture materials)
        - General course questions

        IMPORTANT GUIDELINES:
        1. Only use information from the provided course materials
        2. Do not use outside knowledge.
        3. Always cite sources in square brackets [like this]
        4. If information is not in sources, say "I don't have this information in the course materials"
        5. Be supportive and educational
        6. **CRITICAL:** If the context contains a relevant code snippet, markdown it clearly under a "Relevant Code" section, using the Python language tag (```python...```). Otherwise, omit the "Relevant Code" section.
        7. Never provide direct solutions to active assignments

        CONTEXT:
        {context}

        QUESTION:
        {question}

        Final Answer:
        """
        RAG_PROMPT = ChatPromptTemplate.from_template(template)

        # E. Define the RAG Chain (LCEL)
        RAG_CHAIN = (
            {"context": RETRIEVER, "question": RunnablePassthrough()}
            | RAG_PROMPT
            | llm
            | StrOutputParser()
        )
        print("RAG Chain loaded successfully!")

    except Exception as e:
        print(f"FATAL ERROR during RAG initialization: {e}")
        # In a real app, you might crash the app, but here, log the error.

# Simple Vector Search (The default way LangChain sets up a basic retriever object).
@app.post("/query-rag", tags=["RAG"])
async def query_rag_endpoint(request: QueryRequest):
    """
    Accepts a user question and streams the RAG-augmented answer chunk by chunk.
    The response starts with a metadata block containing sources.
    """
    global RAG_CHAIN
    global RETRIEVER
    
    if RAG_CHAIN is None:
        return {"answer": "Error: RAG system failed to initialize.", "sources": []} # Fallback

    # The content type is typically text/event-stream for SSE, but text/plain is simpler
    # for a basic stream where the client joins the chunks.
    return StreamingResponse(
        stream_rag_answer(request.question, RETRIEVER, RAG_CHAIN), 
        media_type="text/plain" 
    )
'''

@app.post("/query-rag-stream", tags=["RAG"])
async def query_rag_stream_endpoint(request: QueryRequest):
    """
    Accepts a user question and streams the RAG-augmented answer chunk by chunk
    using custom Hybrid Search logic (Vector + Full-Text + RRF).
    """
    # The StreamingResponse handles the asynchronous output from the generator
    return StreamingResponse(
        stream_rag_answer(request.question), 
        media_type="text/plain" 
    )


@app.post("/query-rag", response_model=RAGResponse, tags=["RAG"])
async def query_rag_endpoint(request: QueryRequest):
    """
    Non-streaming endpoint that returns complete answer with sources.
    Uses hybrid search for better relevance across all document types.
    """
    try:
        query = request.question
        
        # Perform hybrid search
        retrieved_documents = hybrid_search(query, limit=5)
        
        if not retrieved_documents:
            return RAGResponse(
                answer="I couldn't find any relevant information in the course materials for your query.",
                sources=[]
            )
        
        # Build context
        context = "\n".join([
            f"{doc['id']}: {doc['text']}" 
            for doc in retrieved_documents[0:5]
        ])
        
        # Get answer from LLM
        response = generation_client.chat.completions.create(
            model=hybrid_retriever.GENERATION_MODEL,
            temperature=0.3,
            messages=[
                {"role": "system", "content": hybrid_retriever.SYSTEM_MESSAGE},
                {"role": "user", "content": f"{query}\n\nContext from course materials:\n{context}"},
            ],
        )
        
        answer = response.choices[0].message.content
        
        # Extract unique sources
        unique_sources = sorted(list(set(
            doc["metadata"]["source"] 
            for doc in retrieved_documents 
            if "source" in doc.get("metadata", {})
        )))
        
        return RAGResponse(answer=answer, sources=unique_sources)
        
    except Exception as e:
        return RAGResponse(
            answer=f"An error occurred while processing your query: {str(e)}",
            sources=[]
        )
    
'''
# --- 2. API Endpoint --- FOR NON-STREAMING (SIMPLE) ---
@app.post("/query-rag", response_model=RAGResponse, tags=["RAG"])
async def query_rag_endpoint(request: QueryRequest):
    """Accepts a user question and returns the RAG-augmented answer and sources."""
    global RAG_CHAIN
    global RETRIEVER

    if RAG_CHAIN is None:
        return {"answer": "Error: RAG system failed to initialize.", "sources": []}

    try:
        query = request.question
        
        # 1. Manually invoke the retriever to get the sources (for logging/UI display)
        # This uses the method you successfully debugged in the last turn
        sources = RETRIEVER.invoke(query) 
        
        # 2. Invoke the full RAG chain for the final answer
        answer = RAG_CHAIN.invoke(query)
        
        # 3. Format sources for the response
        unique_sources = sorted(list(set(d.metadata.get('source') for d in sources)))

        return RAGResponse(
            answer=answer, 
            sources=unique_sources
        )

    except Exception as e:
        return RAGResponse(
            answer=f"An unexpected error occurred during processing: {e}", 
            sources=[]
        )
'''
# --- 3. Simple Health Check ---
@app.get("/health", tags=["System"])
def health_check():
    """Checks if the API is running and the RAG is loaded."""
    # status = "OK" if RAG_CHAIN else "UNINITIALIZED"
    status = "OK" if hybrid_retriever.index else "UNINITIALIZED"
    doc_count = len(hybrid_retriever.documents) if hybrid_retriever.documents else 0
    return {
        "status": status,
        "model": hybrid_retriever.GENERATION_MODEL,
        "indexed_documents": doc_count,
        "search_type": "Hybrid (Vector + Full-Text + RRF + Rerank)",
        "supported_sources": ["PDF", "IPYNB", "CSV"]
    }

# --- DEBUG ENDPOINT: SHOWS RAW CHUNKS ---
@app.get("/debug-chunks")
async def get_raw_chunks(query: str):
    """
    Accepts a query string and returns the raw text and metadata 
    of the top 5 documents retrieved by FAISS.
    """
    global RETRIEVER
    
    if RETRIEVER is None:
        return {"error": "RAG system not initialized."}
        
    try:
        # Retrieve the raw document objects
        sources = RETRIEVER.invoke(query)
        
        # Format the output to be easily readable
        debug_output = []
        for doc in sources:
            debug_output.append({
                "source": doc.metadata.get('source'),
                "chunk_size": len(doc.page_content),
                "raw_content": doc.page_content, # The actual chunk text
            })
            
        return {"query": query, "retrieved_chunks": debug_output}
        
    except Exception as e:
        return {"error": str(e)}


@app.get("/debug-hybrid-search", tags=["Debug"])
async def debug_hybrid_search(query: str):
    """
    Debug endpoint to see how hybrid search retrieves from multi-source FAISS.
    Shows the ranking process and source distribution.
    """
    try:
        retrieved_documents = hybrid_search(query, limit=10)
        
        debug_output = []
        source_count = {}
        
        for i, doc in enumerate(retrieved_documents):
            source = doc.get("metadata", {}).get("source", "unknown")
            source_count[source] = source_count.get(source, 0) + 1
            
            debug_output.append({
                "rank": i + 1,
                "id": doc["id"],
                "source": source,
                "chunk_size": len(doc.get("text", "")),
                "text_preview": doc.get("text", "")[:200] + "..."
            })
        
        return {
            "query": query,
            "total_retrieved": len(retrieved_documents),
            "source_distribution": source_count,
            "retrieved_chunks": debug_output
        }
        
    except Exception as e:
        return {"error": str(e), "query": query}