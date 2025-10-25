import openai
import os
from dotenv import load_dotenv # ⬅️ Import the load_dotenv function

load_dotenv()
print(f"Loaded API Key (first 10 chars): {os.environ.get('OPENROUTER_API_KEY', 'Key Not Found')[:10]}")
api_key=os.environ["OPENROUTER_API_KEY"]
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Test it
response = client.chat.completions.create(
    model=os.environ["GEMINI_MODEL"], 
    messages=[{"role": "user", "content": "Hi"}],
    max_tokens=10
)
print(response.choices[0].message.content)