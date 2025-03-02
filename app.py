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
st.write("### Comentários")
st.markdown(comentario)

# Se há dados, aplicar filtros dinâmicos e gerar gráfico
if not df.empty:
    # Filtros dinâmicos (considera como filtro qualquer coluna que não seja 'time' ou 'value')
    st.sidebar.write("### Filtros Dinâmicos")
    filtros = {}

    colunas_filtro = [col for col in df.columns if col not in ['time', 'value']]

    for coluna in colunas_filtro:
        if coluna == 'geo':
            opcoes = sorted(df[coluna].dropna().unique().tolist())
            selecao = st.sidebar.multiselect(f"Selecione os países ({coluna})",opcoes,default=opcoes[:3])
        elif coluna == 'partner':
            opcoes = sorted(df[coluna].dropna().unique().tolist())
            selecao = st.sidebar.multiselect(f"Selecione os parceiros comerciais ({coluna})", opcoes, default=opcoes[:3])
            filtros[coluna] = selecao
        else:
            opcoes = ["Todos"] + sorted(df[coluna].dropna().unique().tolist())
            selecao = st.sidebar.selectbox(f"Filtrar por {coluna}", opcoes)
            filtros[coluna] = selecao

    # Aplicar filtros no DataFrame
    df_filtrado = df.copy()
    for coluna, selecao in filtros.items():
        if isinstance(selecao,list):
            if selecao:
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(selecao)]
        elif selecao != "Todos":
            df_filtrado = df_filtrado[df_filtrado[coluna] == selecao]

    # Plotly Gráfico Interativo com Legenda Completa
    if not df_filtrado.empty:
        if len(colunas_filtro) > 0:
            # Combina colunas de segmentação para criar uma legenda rica
            df_filtrado['serie_legenda'] = df_filtrado[colunas_filtro].astype(str).agg(' - '.join, axis=1)
            color_coluna = 'serie_legenda'
        else:
            color_coluna = None

        fig = px.line(
            df_filtrado,
            x='time',
            y='value',
            color=color_coluna,
            markers=True,
            title=f"Evolução Temporal - {subtema}",
            labels={'value': 'Valor', 'time': 'Data'}
        )

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.3,  # Isso pode ajustar conforme o tamanho do gráfico e da legenda
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.write("### Dados Filtrados")
        st.dataframe(df_filtrado)


    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

else:
    st.warning("Nenhum dado disponível para este subtema.")


st.write("### Base de Dados")
st.dataframe(df)

