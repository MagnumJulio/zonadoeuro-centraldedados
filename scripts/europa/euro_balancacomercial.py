import requests
import pandas as pd
import itertools
from extracao_eurostat import puxar_dados, salvar_comentario, salvar_base
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openAIapi import analise_descritiva


url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ext_st_easitc?format=JSON&sinceTimePeriod=2019-01&geo=EA20&stk_flow=IMP&stk_flow=EXP&stk_flow=BAL_RT&stk_flow=IMP&stk_flow=EXP&stk_flow=BAL_RT&indic_et=TRD_VAL&indic_et=TRD_VAL&partner=RU&partner=EXT_EA20&partner=US&partner=CN_X_HK&partner=RU&partner=EXT_EA20&partner=US&partner=CN_X_HK&sitc06=TOTAL&sitc06=TOTAL&lang=en"
topico,subtopico = "atividade_economica", "balanca_comercial"
classificacoes = ['stk_flow', 'partner']

def atualizar():

    df = puxar_dados(url)
    comentario = analise_descritiva(df, ' '.join(subtopico.split('_')),classificacoes)

    salvar_base(topico, subtopico, df)
    salvar_comentario(topico, subtopico, comentario)


if __name__ == "__main__":
    atualizar()
    print(f"{subtopico} atualizado(a) e comentário salvo.")

