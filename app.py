import streamlit as st
import requests
import pandas as pd
import itertools
from extracao import puxar_dados
from openAIapi import analise_descritiva

st.set_page_config(page_title="Dashboard Econômico", layout="wide")

assunto = "Taxa de desemprego"
st.title(f"Dashboard Econômico - {assunto} (Eurostat)")

df = puxar_dados()

st.write("Testando OpenAI Key:", st.secrets.get("OPENAI_API_KEY", "NÃO ENCONTREI"))

st.write("### Dados Brutos")
st.dataframe(df)

st.write("### Estatísticas Descritivas")
st.write(df.describe())


st.write("### Descrição")
st.write(analise_descritiva(df,assunto))
