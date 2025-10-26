import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from fastapi import BackgroundTasks # Optional, but good practice
import json
# --- LangChain Imports ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

def stream_rag_answer(query: str, retriever, rag_chain):
    """Retrieves and streams the LLM response."""
    sources = retriever.invoke(query)
    unique_sources = sorted(list(set(d.metadata.get('source') for d in sources)))
    yield f"{{'sources': {json.dumps(unique_sources)}}}" + "[METADATA_END]"

    # 3. Stream the LLM Answer
    for chunk in rag_chain.stream(query):
        # LangChain stream yields the final string chunk by chunk
        yield chunk

# --- 1. Startup Function (Loads Index ONCE) ---
# --- RAG Helper Function (Generator) ---
# This generator function yields chunks of the response as they become available.
def stream_rag_answer(query: str, retriever, rag_chain):
    """Retrieves and streams the LLM response."""
    
    # 1. Retrieve Sources (Done synchronously as it's fast)
    sources = retriever.invoke(query)
    
    # 2. Yield Sources Separator/Metadata first
    # This sends the metadata (sources) to the client *before* the main answer stream starts.
    unique_sources = sorted(list(set(d.metadata.get('source') for d in sources)))
    
    # Use a custom delimiter the front-end can look for to separate metadata from the answer text
    # The JSON structure will be modified to handle the stream, so we send sources first.
    yield f"{{'sources': {json.dumps(unique_sources)}}}" + "[METADATA_END]"

    # 3. Stream the LLM Answer
    for chunk in rag_chain.stream(query):
        # LangChain stream yields the final string chunk by chunk
        yield chunk

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

# --- REVISED STREAMING ENDPOINT ---
# Note: We change the return type to StreamingResponse
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
    status = "OK" if RAG_CHAIN else "UNINITIALIZED"
    return {"status": status, "model": os.getenv("GEMINI_MODEL")}
