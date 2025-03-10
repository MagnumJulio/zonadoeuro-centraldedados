import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_trtu_m?format=JSON&sinceTimePeriod=2019-01&geo=EA20&geo=DE&geo=FR&geo=IT&unit=I21&unit=PCH_PRE&unit=PCH_SM&indic_bt=VOL_SLS&nace_r2=G46&nace_r2=G47_FOOD&nace_r2=G47_NFOOD_X_G473&nace_r2=G473&s_adj=CA&s_adj=SCA&lang=en"
topico,subtopico = "atividade_economica", "vendas_no_varejo"
classificacoes = ['unit', 'geo']

def atualizar():

    df = puxar_dados(url)
    comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)

    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

