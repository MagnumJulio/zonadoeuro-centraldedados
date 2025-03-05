import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io
from scripts.graficos import gerar_grafico_padronizado


st.set_page_config(page_title="Dashboard Econômico", layout="wide")

# Função para ler data da última atualização
def ler_data_atualizacao():
    try:
        with open("datasets/last_update.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Desconhecida"

# Logo e título da sidebar
logo_path = "img/Logomarca Impactus - Azul 2.png"
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.warning("Logomarca não encontrada. Verifique o caminho e o arquivo.")

    st.write("## Central de Dados Econômicos (beta)")
    st.write("""
    Este dashboard apresenta **dados econômicos da Zona do Euro**, 
    organizados por temas e subtemas, com filtros dinâmicos e
    gráficos interativos. Projeto de membros do departamento de Macro Research da Impactus UFRJ.
    """)

    st.write("## 🕒 Última Atualização")
    st.write(f"📅 {ler_data_atualizacao()}")

    st.write("## 🔗 Links Úteis")
    st.markdown("[Eurostat - Site Oficial](https://ec.europa.eu/eurostat)")
    st.markdown("[Relatório do BCE](https://www.ecb.europa.eu/pub/economic-bulletin/html/index.en.html)")
    st.markdown("[GitHub do Projeto](https://github.com)")


st.title(f"Central de dados - Zona do Euro")

# Mapear temas e subtemas
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

temas = mapear_temas_e_subtemas()

# Criar abas para cada tema
abas = list(temas.keys())
tab_selecionada = st.tabs(abas)

# Detectar qual aba está selecionada
for i, tema in enumerate(abas):
    with tab_selecionada[i]:
        st.header(f"{tema}")

        # Seleciona subtema para a aba ativa
        subtema = st.selectbox(f"Selecione o subtema ({tema})", temas[tema], key=f"subtema_{tema}")

        # Função para carregar dados e comentários
        def carregar_dados(tema, subtema):
            tema_path = tema.lower().replace(" ", "_")
            subtema_path = subtema.lower().replace(" ", "_")

            csv_path = f"datasets/{tema_path}/{subtema_path}_historico.csv"
            md_path = f"datasets/{tema_path}/{subtema_path}_comentarios.md"
            # print(csv_path+"\n"+md_path)
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

        df, comentario = carregar_dados(tema, subtema)
        if tema == "Sentimento Economico":
            print(df)
        st.write("### Comentários")
        st.markdown(comentario)

        # Filtros dinâmicos e gráficos apenas se há dados
        if not df.empty:
            filtros = {}

            colunas_filtro = [col for col in df.columns if col not in ['time', 'value']]

            for coluna in colunas_filtro:
                if coluna == 'geo':
                    opcoes = sorted(df[coluna].dropna().unique().tolist())
                    selecao = st.multiselect(f"Selecione os países ({coluna})", opcoes, default=opcoes[:3], key=f"{tema}_{subtema}_geo")
                    filtros[coluna] = selecao
                elif coluna == 'partner':
                    opcoes = sorted(df[coluna].dropna().unique().tolist())
                    selecao = st.multiselect(f"Selecione os parceiros comerciais ({coluna})", opcoes, default=opcoes[:3], key=f"{tema}_{subtema}_partner")
                    filtros[coluna] = selecao
                else:
                    opcoes = ["Todos"] + sorted(df[coluna].dropna().unique().tolist())
                    selecao = st.selectbox(f"Filtrar por {coluna}", opcoes, key=f"{tema}_{subtema}_{coluna}")
                    filtros[coluna] = selecao

            # Aplicar filtros
            df_filtrado = df.copy()

            for coluna, selecao in filtros.items():
                if isinstance(selecao, list):
                    if selecao:
                        df_filtrado = df_filtrado[df_filtrado[coluna].isin(selecao)]
                elif selecao != "Todos":
                    df_filtrado = df_filtrado[df_filtrado[coluna] == selecao]

            colunas_legenda = []
            subtitulo_partes = []

            for coluna in colunas_filtro:
                valores_unicos = df_filtrado[coluna].unique()
                if len(valores_unicos) == 1:
                    subtitulo_partes.append(f"{coluna.replace('_', ' ').title()}: {valores_unicos[0]}")
                else:
                    colunas_legenda.append(coluna)

            subtitulo = " | ".join(subtitulo_partes)

            if not df_filtrado.empty:
                if colunas_legenda:
                    df_filtrado['serie_legenda'] = df_filtrado[colunas_legenda].astype(str).agg(' - '.join, axis=1)
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

                if subtitulo:
                    fig.update_layout(
                        annotations=[dict(
                            text=subtitulo,
                            showarrow=False,
                            x=0.5,
                            y=1.08,
                            xref="paper",
                            yref="paper",
                            align="center",
                            font=dict(size=12)
                        )]
                    )

                fig.update_layout(
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.3,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

                st.write("### Dados Filtrados")
                csv_buffer = io.StringIO()
                df_filtrado.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Baixar Dados Filtrados (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"{subtema.lower().replace(' ', '_')}_dados_filtrados.csv",
                    mime="text/csv"
                )

                # Monta título sugerido (subtema + classificações únicas)
                titulo_sugerido = f"Evolução Temporal - {subtema}"
                if subtitulo_partes:
                    titulo_sugerido += "\n" + " | ".join(subtitulo_partes)

                # Input editável de título
                titulo_final = st.text_input("Título do Gráfico", value=titulo_sugerido, key=f"titulo_{tema}_{subtema}")

                # Janela temporal e botão de geração
                min_date = st.date_input("Data inicial", value=df_filtrado['time'].min(), min_value=df_filtrado['time'].min(), max_value=df_filtrado['time'].max(), key=f"min_date_{tema}_{subtema}")
                max_date = st.date_input("Data final", value=df_filtrado['time'].max(), min_value=df_filtrado['time'].min(), max_value=df_filtrado['time'].max(), key=f"max_date_{tema}_{subtema}")

                if st.button("Gerar Gráfico Padronizado", key=f"btn_grafico_{tema}_{subtema}"):
                    gerar_grafico_padronizado(df_filtrado, subtema, min_date, max_date, titulo=titulo_final)

            else:
                st.warning("Nenhum dado disponível para os filtros selecionados.")
        else:
            st.warning("Nenhum dado disponível para este subtema.")

        st.write("### Base de Dados Completa")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Baixar Dados Completos (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"{subtema.lower().replace(' ', '_')}_dados.csv",
            mime="text/csv"
        )

        