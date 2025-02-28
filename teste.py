import os
import openai

print("🔑 OpenAI Key encontrada?", "Sim" if os.getenv("OPENAI_API_KEY") else "Não")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.models.list()
    print("✅ Modelos disponíveis:", [model.id for model in response.data])
except Exception as e:
    print(f"❌ Erro ao listar modelos: {e}")
