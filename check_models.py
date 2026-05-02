import google.generativeai as genai

# Replace with your actual key
genai.configure(api_key="AIzaSyDUeqF2FuunPe54qHdH_mJQXvGw6u6LTno")

print("Models available for text generation:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)