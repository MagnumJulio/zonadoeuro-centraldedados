import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m?format=JSON&sinceTimePeriod=2019-01&geo=EA20&geo=DE&geo=FR&unit=PC_ACT&s_adj=SA&age=TOTAL&age=Y_LT25&age=Y25-74&sex=T&sex=M&sex=F&lang=en"
topico,subtopico = "mercado_de_trabalho", "taxa_de_desemprego"
classificacoes = ['sex', 'geo']

def atualizar():

    df = puxar_dados(url)
    # comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)
    print(df)
    salvar_base(topico, subtopico, df)
    # salvar_comentario(topico, subtopic    print(df)o, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

