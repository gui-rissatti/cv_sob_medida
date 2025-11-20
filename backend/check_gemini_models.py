"""Check available Gemini models via Google AI API."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.config import get_settings
import google.generativeai as genai

settings = get_settings()

if not settings.google_api_key:
    print("❌ GOOGLE_API_KEY not found in settings!")
    sys.exit(1)

print("🔑 API Key configured successfully")
print(f"Key preview: {settings.google_api_key[:10]}...{settings.google_api_key[-4:]}")
print("\n" + "=" * 80)
print("AVAILABLE GEMINI MODELS")
print("=" * 80)

genai.configure(api_key=settings.google_api_key)

try:
    models = genai.list_models()
    
    print("\n✅ Successfully connected to Google AI API\n")
    
    generation_models = []
    for model in models:
        # Check if model supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            generation_models.append(model)
            print(f"📦 Model: {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Supported methods: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("=" * 80)
    print(f"Total models supporting generateContent: {len(generation_models)}")
    print("=" * 80)
    
    if generation_models:
        print("\n✅ RECOMMENDED MODELS FOR LANGCHAIN:\n")
        for model in generation_models[:5]:  # Show top 5
            # Extract model ID (remove 'models/' prefix)
            model_id = model.name.replace('models/', '')
            print(f"   - {model_id}")
    
except Exception as e:
    print(f"\n❌ Error connecting to Google AI API:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
