import streamlit as st
import openai

# OpenAI

def analise_descritiva(df, assunto):
    api_key = st.secrets["OPENAI_API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    # Encontrar as duas últimas datas
    ultimas_datas = df['time'].tail(3)

    # Filtrar usando loc[]
    df_filtrado = df.loc[df['time'].isin(ultimas_datas)]

    # Exibir preview
    str1 = df.describe().to_string()
    str2 = df.tail().describe().to_string()
    texto = 'Describe dados gerais:\n'+str1+'\nDescribe dados mais recentes:\n'+str2+'\nUltimos dois meses por cada decomposição:\n'+df_filtrado.to_string(index=False)

    prompt = f"""
Você é um economista experiente. Com base nos dados de {assunto} abaixo, escreva uma breve análise descritiva para incluir em um relatório econômico.(obs inicial: i-valores decimais até 2 digitos e nao precisa detlhar valores de dados gerais, apenas os últimos dados; ii-seja objetivo, nao tente escrever muito, quero dinâmica, e nao quero sugestões de políticas, apenas a analise descritiva; iii-quero uma análise para mercado financeiro, vamos pensar em lucros, rotação setorial, etc. nao uma analise para um policy maker) 1) Os últimos dados estão indicando aumento, baixa ou estabilização? 2) Relacione qualitativamente os últimos dados com a media e a variação geral da série (se atualmente está mais estável/acomodado, se está acima ou abaixo da média,etc. 3) analisar as subcategorias dos dados. Máximo 3 parágrafos (500 palavras), apenas o essencial.

{texto}
    """

    resposta = openai.Client().chat.completions.create(

        model="gpt-4o-2024-08-06",
        messages=[{"role":"system", "content": "Você é um analista econômico"},
                  {"role": "user", "content": prompt}],
        temperature=1
        
    )

    return resposta.choices[0].message.content

