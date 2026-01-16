import os
from google import genai
from dotenv import load_dotenv

# 1. Load the "Secret Box"
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize The Client
client = genai.Client(api_key=api_key)

# 3. Use the LATEST 2026 model: gemini-3-flash-preview
try:
    response = client.models.generate_content(
        model='gemini-3-flash-preview', 
        contents="Explain RAG Agents to me like I am a 5-year-old."
    )
    print("--- Gemini 3 Response ---")
    print(response.text)
except Exception as e:
    print(f"\n[SYSTEM NOTE]: Still waiting for Google to activate your billing.")
    print(f"Error details: {e}")