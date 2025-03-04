import pandas as pd

# print("🔑 OpenAI Key encontrada?", "Sim" if os.getenv("OPENAI_API_KEY") else "Não")

# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# try:
#     response = client.models.list()
#     print("✅ Modelos disponíveis:", [model.id for model in response.data])
# except Exception as e:
#     print(f"❌ Erro ao listar modelos: {e}")

csv_path = "datasets/sentimento_economico/confianca_do_consumidor_historico.csv"
df = pd.read_csv(csv_path)
print(df)