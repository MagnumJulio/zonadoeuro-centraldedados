import streamlit as st
import requests
import pandas as pd
import itertools
from extracao import puxar_dados
from openAIapi import analise_descritiva

st.set_page_config(page_title="Dashboard Econômico", layout="wide")

st.title("Dashboard Econômico - Produção Industrial (Eurostat)")

df = puxar_dados()

st.write("### Dados Brutos")
st.dataframe(df)

st.write("### Estatísticas Descritivas")
st.write(df.describe())

api_key = st.secrets["OPENAI_API_KEY"]
st.write("### Descrição")
st.write(analise_descritiva(df, api_key))
