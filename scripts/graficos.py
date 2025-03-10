import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

CORES_PADRONIZADAS = ["#082631", "#166083", "#37A6D9", "#AFABAB", "#82C1DB"]

def gerar_legenda_e_titulo(df, subtema):
    colunas_excluidas = {'freq', 'sitc06', 'time', 'value'}
    if 'serie_legenda' in df.columns:
        colunas_legenda = []
        titulo_partes = []
        for coluna in df.columns:
            if coluna in colunas_excluidas or coluna == 'serie_legenda':
                continue
            valores_unicos = df[coluna].dropna().unique()
            if len(valores_unicos) == 1:
                titulo_partes.append(f"{coluna.replace('_', ' ').title()}: {valores_unicos[0]}")
            else:
                colunas_legenda.append(coluna)
        titulo = f"{subtema}"
        if titulo_partes:
            titulo += "\n" + " | ".join(titulo_partes)
        return df, titulo
    
    colunas_legenda = []
    titulo_partes = []
    for coluna in df.columns:
        if coluna in colunas_excluidas:
            continue
        valores_unicos = df[coluna].dropna().unique()
        if len(valores_unicos) == 1:
            titulo_partes.append(f"{coluna.replace('_', ' ').title()}: {valores_unicos[0]}")
        else:
            colunas_legenda.append(coluna)
    titulo = f"{subtema}"
    if titulo_partes:
        titulo += "\n" + " | ".join(titulo_partes)
    if len(colunas_legenda) == 1:
        df['serie_legenda'] = df[colunas_legenda[0]].astype(str)
    elif len(colunas_legenda) > 1:
        df['serie_legenda'] = df[colunas_legenda].astype(str).agg(' - '.join, axis=1)
    else:
        df['serie_legenda'] = 'Série Única'
    return df, titulo

def gerar_grafico_padronizado(df, subtema, data_inicial=None, data_final=None, titulo=None, label=None):
    if df.empty:
        st.error("Nenhum dado disponível para gerar o gráfico.")
        return
    if data_inicial and data_final:
        df = df[(df['time'] >= data_inicial) & (df['time'] <= data_final)]
    if not titulo:
        df, titulo = gerar_legenda_e_titulo(df, subtema)
    else:
        df, _ = gerar_legenda_e_titulo(df, subtema)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    series_unicas = df['serie_legenda'].unique()
    for idx, serie in enumerate(series_unicas):
        cor = CORES_PADRONIZADAS[idx % len(CORES_PADRONIZADAS)]
        dados_serie = df[df['serie_legenda'] == serie]
        ax.plot(dados_serie['time'], dados_serie['value'], label=serie, color=cor, linewidth=2)
    
    # Configuração do título principal
    ax.set_title(titulo, fontsize=14, fontweight='bold', color='black', pad=10)
    
    # Adição do label abaixo do título
    if label:
        fig.text(0.5, 0.91, label, ha='center', fontsize=10, color='darkgray', style='italic')
    
    ax.set_xlabel("Data", fontsize=10)
    ax.set_ylabel("Valor", fontsize=10)
    ax.grid(False)
    
    ax.legend(
        loc="upper center",
        ncol=min(len(series_unicas), 3),
        frameon=False,
        fontsize=9
    )
    
    fig.text(0.5, -0.05, "Fonte: Eurostat, Impactus UFRJ", ha='center', fontsize=9, color='gray')
    
    st.pyplot(fig)

# Exemplo de uso
# df_exemplo = pd.DataFrame({
#     'time': pd.date_range(start='2020-01-01', periods=10, freq='M'),
#     'value': [10, 15, 13, 17, 20, 18, 22, 25, 23, 28],
#     'regiao': ['Europa', 'Europa', 'Europa', 'Europa', 'Europa', 'Europa', 'Europa', 'Europa', 'Europa', 'Europa'],
#     'industria': ['Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva', 'Automotiva']
# })
# gerar_grafico_padronizado(df_exemplo, "Exportações", label="Crescimento Trimestral (2020-2021)")