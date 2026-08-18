import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env properly
load_dotenv()

# Get key
API_KEY = os.getenv("GEMINI_API_KEY")

print("KEY:", API_KEY)  # debug

genai.configure(api_key=API_KEY)

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)