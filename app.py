import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(page_title="Dashboard Econômico", layout="wide")
st.title(f"Central de dados - Zona do Euro")

def mapear_temas_e_subtemas(base_dir="datasets"):
    temas = {}
    for tema in os.listdir(base_dir):
        tema_path = os.path.join(base_dir, tema)
        if os.path.isdir(tema_path):
            subtemas = []
            for arquivo in os.listdir(tema_path):
                if arquivo.endswith("_historico.csv"):
                    subtema = arquivo.replace("_historico.csv", "").replace("_", " ").title()
                    subtemas.append(subtema)
            temas[tema.replace("_", " ").title()] = subtemas
    return temas

# Carregar temas e subtemas dinamicamente
temas = mapear_temas_e_subtemas()

# Seleção de tema e subtema
tema = st.sidebar.selectbox("Selecione o tema", list(temas.keys()))
subtema = st.sidebar.selectbox("Selecione o subtema", temas[tema])

st.header(f"{tema} - {subtema}")

# Função para carregar dados e comentário
def carregar_dados(tema, subtema):
    tema_path = tema.lower().replace(" ", "_")
    subtema_path = subtema.lower().replace(" ", "_")

    csv_path = f"datasets/{tema_path}/{subtema_path}_historico.csv"
    md_path = f"datasets/{tema_path}/{subtema_path}_comentarios.md"

    try:
        df = pd.read_csv(csv_path)
        df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.date
        with open(md_path, "r", encoding="utf-8") as f:
            comentario = f.read()
    except FileNotFoundError:
        st.error(f"Arquivos para '{subtema}' não encontrados.")
        df = pd.DataFrame()
        comentario = "Nenhum comentário disponível."

    return df, comentario

# Carregar dados e comentários do subtema selecionado
df, comentario = carregar_dados(tema, subtema)

# Mostrar DataFrame e Comentário
st.write("### Base de Dados")
st.dataframe(df)

st.write("### Comentário Atualizado")
st.markdown(comentario)

# Filtros dinâmicos (automáticos)
st.sidebar.write("### Filtros Dinâmicos")
filtros = {}

# Considera como filtro qualquer coluna que não seja 'time' ou 'value'
colunas_filtro = [col for col in df.columns if col not in ['time', 'value']]

for coluna in colunas_filtro:
    opcoes = ["Todos"] + sorted(df[coluna].dropna().unique().tolist())
    selecao = st.sidebar.selectbox(f"Filtrar por {coluna}", opcoes)
    filtros[coluna] = selecao

# Aplicar os filtros automaticamente
df_filtrado = df.copy()
for coluna, selecao in filtros.items():
    if selecao != "Todos":
        df_filtrado = df_filtrado[df_filtrado[coluna] == selecao]

# Mostrar a base filtrada
st.write("### Dados Filtrados")
st.dataframe(df_filtrado)

# Gráfico interativo
if len(df_filtrado) > 0:
    fig = px.line(
        df_filtrado,
        x='time',
        y='value',
        color=colunas_filtro[0] if colunas_filtro else None,
        markers=True,
        title=f"Evolução Temporal - {subtema}",
        labels={'value': 'Valor', 'time': 'Data'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum dado disponível para os filtros selecionados.")

