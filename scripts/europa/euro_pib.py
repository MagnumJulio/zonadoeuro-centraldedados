import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_gdp?format=JSON&sinceTimePeriod=2019-Q1&geo=EA20&geo=DE&geo=FR&geo=IT&unit=CLV_PCH_PRE&unit=CLV_PCH_SM&unit=CLV_PCH_ANN&s_adj=SCA&na_item=B1GQ&lang=en"
topico,subtopico = "atividade_economica", "pib"
classificacoes = ['na_item', 'geo']

def atualizar():

    df = puxar_dados(url)
    print(df)
    comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)

    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

