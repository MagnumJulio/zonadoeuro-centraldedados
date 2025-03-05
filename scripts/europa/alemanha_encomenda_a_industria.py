import pandas as pd
import os
import sys
from datetime import datetime

# Importando do extracao_investing.py
from extracao_investing import extrair_tabela_investing, salvar_base, salvar_comentario

# Caminho dinâmico para importar openAIapi
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva

# Definindo tema e subtema
topico, subtopico = "atividade_economica", "encomendas_industria_alemanha"

# URL específica do Investing para Confiança do Consumidor
url = "https://br.investing.com/economic-calendar/german-factory-orders-130"

# Colunas/classificações para análise descritiva (nesse caso, só tem o valor mesmo)
classificacoes = []  # Se quiser adicionar algo no futuro (exemplo: país), aqui ficaria

def atualizar():
    # Puxa dados diretamente do Investing
    df = extrair_tabela_investing(url, tema=topico, subtema=subtopico)

    if df is None or df.empty:
        print(f"❌ Falha ao atualizar '{subtopico}'. Nenhum dado retornado.")
        return

    # 🔥 Limpeza adicional (remover linhas com campos críticos vazios)
    df = df.dropna(subset=['time', 'tipo', 'value'])
    df = df[df['value'] != '']

    if df.empty:
        print(f"⚠️ Nenhum dado válido após limpeza para '{subtopico}'.")
        return

    # Gera comentário com OpenAI (ajuste se necessário)
    comentario = analise_descritiva(df, subtopico.replace('_', ' '), classificacoes)

    # Salva base e comentário
    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)

    print(f"✅ '{subtopico}' atualizado e comentário salvo.")


if __name__ == "__main__":
    atualizar()
