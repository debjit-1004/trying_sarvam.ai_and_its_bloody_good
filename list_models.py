import google.generativeai as genai
import os

# Configure with API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# List available models
print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")
