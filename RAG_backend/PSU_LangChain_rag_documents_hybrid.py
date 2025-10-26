import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings # ChatOpenAI will be used to talk to Gemini via OpenRouter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)
# --- 1. CONFIGURATION ---
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
EMBEDDING_MODEL = "text-embedding-3-small" # Must match ingestion script!
GENERATION_MODEL = os.getenv("GEMINI_MODEL", "google/gemini-2.5-flash")

# --- 2. LOAD COMPONENTS ---

# A. Load Embeddings Client (Required to load the FAISS index)
embedding_client = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_KEY"], # Using direct OpenAI for stability
    model=EMBEDDING_MODEL
)

# B. Load Vector Store and set up Retriever
print("Loading FAISS index...")
vectorstore = FAISS.load_local(
    "faiss_index_hackpsu", 
    embedding_client, 
    allow_dangerous_deserialization=True # Required when loading from disk
)
print(f"SUCCESS: FAISS Index loaded. Contains {vectorstore.index.ntotal} total documents (chunks).")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # powerful vector similarity search.Retrieve top 5 most relevant chunks

# C. Load Generative Model (Gemini via OpenRouter)
print(f"Connecting to Generator: {GENERATION_MODEL}")
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY,
    model=GENERATION_MODEL
)

SYSTEM_MESSAGE = """
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
RAG_PROMPT = ChatPromptTemplate.from_template(SYSTEM_MESSAGE)

# --- 4. THE RAG CHAIN (LCEL) ---
# LCEL chains the steps: Context -> Retrieval -> Prompt -> LLM -> Output
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

def run_query(query: str):
    print(f"\nSearching course materials for: '{query}'...")
    response = rag_chain.invoke(query)
    
    # Optional: Display the sources retrieved for transparency
    # This requires running the retriever separately, but the simple chain works faster:
    # sources = retriever.get_relevant_documents(query)
    # print("--- Retrieved Source Files ---")
    # print([d.metadata['source'] for d in sources])

    sources = retriever._get_relevant_documents(query)
    print("\n AI Answer:")
    print(response)
    
    print("\n Sources Cited:")
    # Print unique sources to match the old format
    unique_sources = sorted(list(set(d.metadata.get('source') for d in sources)))
    for source in unique_sources:
        print(f"- {source}")
    print("-" * 50)


# Test the specific, context-rich questions
# run_query("Explain how training an RNN works, referencing the concept of backpropagation through time.")
# run_query("What is the TA's email address and what assignment is due next week?")
# run_query("Who invented the light bulb?") 
run_query("What example or code he used to explain Mini batch Gradient descent ?")
run_query("when did he teach about Mini batch Gradient descent?")