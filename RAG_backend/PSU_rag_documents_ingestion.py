import json
import os
import pathlib
import time
import azure.identity
import openai
import pymupdf4llm
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, NotebookLoader 
from langchain_openai import OpenAIEmbeddings # Use this for OpenRouter embeddings
from langchain_community.vectorstores import FAISS 
from langchain_community.document_loaders import CSVLoader

load_dotenv(override=True)

API_HOST = os.getenv("API_HOST", "github")
print(f"API_HOST: {API_HOST}")


# Embedding client (OpenAI - for reliability)
# Uncomment the following to use OpenAI embedding model
# embedding_client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
EMBEDDING_MODEL = "text-embedding-3-small" 
# EMBEDDING_MODEL = "google/embedding-001"

# Use the LangChain wrapper configured for OpenRouter
embedding_client = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_KEY"], # Use the direct key
    model=EMBEDDING_MODEL,
)
print(f"Embeddings: OpenAI {EMBEDDING_MODEL}")

# Generation client (Gemini via OpenRouter - for generation later)
generation_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)
GENERATION_MODEL = os.getenv("GEMINI_MODEL", "google/gemini-2.0-flash-exp")
print(f"Generation: Gemini {GENERATION_MODEL}\n")

data_dir = pathlib.Path(os.path.dirname(__file__)) / "data"
# filenames= ['PSU_Syllabus_IA651_Spring_2025.pdf']
filenames=['PSU_Syllabus_IA651_Spring_2025.pdf','2025_01_IA651CourseSchedule.csv','01.ipynb','02.ipynb','03.ipynb','04.ipynb','05.ipynb','06.ipynb']
all_chunks = []
all_docs = []
 # Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    model_name="gpt-4o", chunk_size=500, chunk_overlap=125
)

for filename in filenames:
    file_path = data_dir / filename
    if filename.endswith(".pdf"):
        # md_text = pymupdf4llm.to_markdown(data_dir / filename)
        loader = PyMuPDFLoader(file_path)
    elif filename.endswith(".csv"): 
        print(f"Loading CSV: {filename}")
        # The loader treats each row as a separate document
        loader = CSVLoader(file_path=file_path, encoding="utf8")
    elif filename.endswith(".ipynb"):
        print(f"Loading Notebook: {filename}")
        loader = NotebookLoader(file_path, include_outputs=False)
    elif filename.endswith(".txt"):
        # with open(file_path, "r", encoding="utf-8") as file:
        #     md_text = file.read()
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type for file: {filename}")
        continue
   
    # texts = text_splitter.create_documents([md_text])
    documents = loader.load()
    split_docs = text_splitter.split_documents(documents)
    for doc in split_docs:
        doc.metadata["source"] = filename
    
    print(f" -> {filename} split into {len(split_docs)} chunks.")
    all_docs.extend(split_docs)
'''
    total_chunks = len(texts)
    file_chunks = []
    chunk_index = 0

    # CHUNK COUNT LOG:
    print(f"   -> Document split into {total_chunks} chunks. Starting embedding API calls...")

    # Use a while loop with an index to guarantee retries
    while chunk_index < total_chunks:
        text = texts[chunk_index]
        chunk_data = {
            "id": f"{filename}-{(chunk_index + 1)}", 
            "text": text.page_content,
            "metadata": {
                "source": filename,
                "chunk_index": chunk_index + 1,
                "total_chunks": total_chunks
            }
        }
        try:
            # CHUNK EMBEDDING LOG:
            print(f"      [Chunk {chunk_index + 1}/{total_chunks}] Calling API...")
            
            chunk_data["embedding"] = (
                embedding_client.embeddings.create(model=EMBEDDING_MODEL, input=chunk_data["text"]).data[0].embedding
            )
            
            # SUCCESS LOG AND PAUSE:
            print(f"      [Chunk {chunk_index + 1}/{total_chunks}] SUCCESS. Pausing for 5 seconds to manage rate limit...")
            time.sleep(5) 
            
            # Success: Append data and increment the index to move to the next chunk
            file_chunks.append(chunk_data)
            chunk_index += 1 
            
        except openai.RateLimitError:
            print(f"      [Chunk {chunk_index + 1}/{total_chunks}] !!! RATE LIMIT HIT. Pausing for 30 seconds to recover...")
            time.sleep(30)
            continue # Restart the while loop for the same chunk_index
            
        except Exception as e:
            print(f"      [Chunk {chunk_index + 1}/{total_chunks}] !!! UNEXPECTED ERROR: {e}. Skipping this chunk.")
            chunk_index += 1 # Increment index to move past the problematic chunk
            
    all_chunks.extend(file_chunks)
    '''
print("\nStarting embedding and FAISS indexing...")

# FAISS handles the embedding calls and storage efficiently
vectorstore = FAISS.from_documents(
    all_docs, 
    embedding=embedding_client 
)

# You can save the vector store to disk (optional, but good practice)
vectorstore.save_local("faiss_index_hackpsu")

print(f"\n All documents loaded and indexed into 'faiss_index_hackpsu' with {len(all_docs)} total chunks.")

# Save the documents with embeddings to a JSON file
with open("PSU_notebooks_rag_ingested_chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=4)
