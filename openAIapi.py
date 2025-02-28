import streamlit as st
import openai

# OpenAI

def analise_descritiva(df):
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
Você é um economista experiente. Com base nos dados abaixo, escreva uma breve análise descritiva para incluir em um relatório econômico. Inclua leves comentários sobre tendências, mas concentre-se nos dados totais/gerais para depois analisar suas decomposições. Máximo 3 parágrafos (500 palavras), apenas o essencial.

{texto}
    """

    resposta = openai.Client().chat.completions.create(

        model="gpt-4",
        messages=[{"role":"system", "content": "Você é um analista econômico"},
                  {"role": "user", "content": prompt}],
        temperature=0.7
        
    )

    return resposta.choices[0].message.content

