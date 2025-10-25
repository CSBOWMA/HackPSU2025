import json
import os
import pathlib
import time
import azure.identity
import openai
import pymupdf4llm
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(override=True)

API_HOST = os.getenv("API_HOST", "github")
print(f"API_HOST: {API_HOST}")


# Embedding client (OpenAI - for reliability)
embedding_client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
EMBEDDING_MODEL = "text-embedding-3-small"
print(f"Embeddings: OpenAI {EMBEDDING_MODEL}")

# Generation client (Gemini via OpenRouter - for generation later)
generation_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)
GENERATION_MODEL = os.getenv("GEMINI_MODEL", "google/gemini-2.0-flash-exp")
print(f"Generation: Gemini {GENERATION_MODEL}\n")


data_dir = pathlib.Path(os.path.dirname(__file__)) / "data"
filenames= ['PSU_Syllabus_IA651_Spring_2025.pdf']
all_chunks = []
for filename in filenames:
    file_path = data_dir / filename
    if filename.endswith(".pdf"):
        md_text = pymupdf4llm.to_markdown(data_dir / filename)
    elif filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            md_text = file.read()
    else:
        raise ValueError(f"Unsupported file type for file: {filename}")
    # Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o", chunk_size=500, chunk_overlap=125
    )
    texts = text_splitter.create_documents([md_text])
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

# Save the documents with embeddings to a JSON file
with open("PSU_rag_ingested_chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=4)
