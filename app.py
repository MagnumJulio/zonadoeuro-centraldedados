import streamlit as st
import requests
import pandas as pd
import itertools

st.set_page_config(page_title="Dashboard Econômico", layout="wide")

api_key = st.secrets["OPENAI_API_KEY"]

st.title("Dashboard Econômico - Produção Industrial (Eurostat)")

url = st.text_input("Cole o link da API da Eurostat aqui:")

if url:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        dimensions = data['dimension']

        def extract_categories(dimension):
            return list(dimension['category']['index'].keys())

        def get_labels(dimension):
            return dimension['category']['label']

        freq = extract_categories(dimensions['freq'])
        indic_bt = extract_categories(dimensions['indic_bt'])
        nace_r2 = extract_categories(dimensions['nace_r2'])
        s_adj = extract_categories(dimensions['s_adj'])
        unit = extract_categories(dimensions['unit'])
        geo = extract_categories(dimensions['geo'])
        time = extract_categories(dimensions['time'])

        freq_labels = get_labels(dimensions['freq'])
        indic_bt_labels = get_labels(dimensions['indic_bt'])
        nace_r2_labels = get_labels(dimensions['nace_r2'])
        s_adj_labels = get_labels(dimensions['s_adj'])
        unit_labels = get_labels(dimensions['unit'])
        geo_labels = get_labels(dimensions['geo'])
        time_labels = get_labels(dimensions['time'])

        combinations = list(itertools.product(
            freq, indic_bt, nace_r2, s_adj, unit, geo, time
        ))

        rows = []
        values = data.get("value", {})

        for idx, comb in enumerate(combinations):
            rows.append({
                'freq': freq_labels[comb[0]],
                'indic_bt': indic_bt_labels[comb[1]],
                'nace_r2': nace_r2_labels[comb[2]],
                's_adj': s_adj_labels[comb[3]],
                'unit': unit_labels[comb[4]],
                'geo': geo_labels[comb[5]],
                'time': time_labels[comb[6]],
                'value': values.get(str(idx), None)
            })

        df = pd.DataFrame(rows)

        st.write("### Dados Brutos")
        st.dataframe(df)

        st.write("### Estatísticas Descritivas")
        st.write(df.describe())

        st.line_chart(df.pivot(index='time', columns='nace_r2', values='value'))

    except Exception as e:
        st.error(f"Erro ao buscar ou processar os dados: {e}")