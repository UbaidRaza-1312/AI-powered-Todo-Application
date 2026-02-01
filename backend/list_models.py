import google.generativeai as genai
import os

# Configure with the API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# List all available models
print("Available models:")
for model in genai.list_models():
    print(f"Name: {model.name}")
    print(f"Description: {model.description}")
    print(f"Input Token Limit: {model.input_token_limit}")
    print(f"Output Token Limit: {model.output_token_limit}")
    print(f"Supported Generation Methods: {model.supported_generation_methods}")
    print("---")