import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr?format=JSON&sinceTimePeriod=2019-01&geo=EA&geo=DE&geo=FR&geo=IT&unit=RCH_A&coicop=CP00&coicop=FOOD&coicop=IGD_NNRG&coicop=NRG&coicop=SERV&coicop=TOT_X_NRG_FOOD&lang=en"
topico,subtopico = "inflacao", "hicp"
classificacoes = ['coicop', 'geo']

def atualizar():

    df = puxar_dados(url)
    comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)

    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

