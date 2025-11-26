import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega sua chave
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("=== Modelos Disponíveis para sua Chave ===")
try:
    for m in genai.list_models():
        # Filtra apenas modelos que geram conteúdo (texto/visão)
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")