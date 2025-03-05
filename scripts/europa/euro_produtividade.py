import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/namq_10_lp_ulc?format=JSON&sinceTimePeriod=2019-Q1&geo=EA20&geo=DE&geo=FR&geo=IT&unit=I20&unit=PCH_PRE&unit=PCH_SM&s_adj=SCA&na_item=RLPR_PER&na_item=RLPR_HW&lang=en"
topico,subtopico = "mercado_de_trabalho", "produtividade"
classificacoes = ['na_item', 'unit', 'geo']

def atualizar():

    df = puxar_dados(url)
    comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)

    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

