import streamlit as st
import openai
import datetime
import pandas as pd

# OpenAI

def analise_descritiva(df, assunto, colunas_classificadoras):
    api_key = st.secrets["OPENAI_API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    print(assunto)
    if assunto == "hicp" and "geo" in df.columns:
        df = df.loc[df['geo'] == "Euro area (EA11-1999, EA12-2001, EA13-2007, EA15-2008, EA16-2009, EA17-2011, EA18-2014, EA19-2015, EA20-2023)"]


    # Encontrar as duas últimas datas
    ultimas_datas = df['time'].tail(2)


    if (colunas_classificadoras):
        df_filtrado = df.copy()
        # Estatísticas gerais
        str1 = df.describe().to_string()
        describe_historico = df.groupby(colunas_classificadoras)['value'].describe()
        str1 = describe_historico.to_string()
        print(describe_historico)

        # Estatísticas por grupo (dinâmico)
        describe_grupo = df_filtrado.groupby(colunas_classificadoras)['value'].describe()
        str2 = describe_grupo.to_string()
        print(describe_grupo)
    else:
        df_filtrado = df.loc[df['time'].isin(ultimas_datas)]
        str1 = df.to_string()
        str2 = df_filtrado.to_string()

    texto = 'Describe dados gerais:\n'+str1+'\nDescribe dados mais recentes:\n'+str2+'\nUltimos meses por cada decomposição:\n'+df_filtrado.to_string(index=False)

    prompt = f"""
Você é um economista experiente. Com base nos dados de {assunto} abaixo, escreva uma breve análise descritiva para incluir em um relatório econômico.
obs inicial: 
i-valores decimais até 2 digitos depois da vírgula e nao precisa detlhar valores de dados gerais, apenas os últimos dados; 
ii-seja objetivo, nao tente escrever muito, quero dinâmica, e nao quero sugestões de políticas, apenas a analise descritiva; 
iii-destaque em negrito **dessa forma** na string de resposta.
---
1) Os últimos dados estão indicando aumento, baixa ou estabilização? 
1.1) É muito importante que você não confunda direções (alta/baixa). Valores negativos indicam piora caso aumentem seu módulo.
2) Relacione qualitativamente os últimos dados com a media e a variação geral da série (se atualmente está mais estável/acomodado, se está acima ou abaixo da média,etc. 
3) analisar as subcategorias dos dados. Máximo 2 parágrafos!! (100 palavras).
---
Modelo de input (exemplo com inflação, mas a estrutura pode ser semelhante com outras variáveis)

[
O dado cheio do PCE avançou 0,33% m/m em janeiro, enquanto o núcleo subiu 0,25% m/m. Isso provocou a **desaceleração do dado anual para 2,5%, contudo o
momentum de 3 meses ainda apresenta tendência de alta**, o que mantém acesa a nossa preocupação em
relação à inflação.
O setor de **serviços avançou 0,25% m/m**, um número menor em relação à média das leituras de 2024. Esse
é um bom sinal, considerando que no último ano, o setor foi a maior complicação para o avanço da inflação
à meta do FED. Já a parte de **bens avançou 0,6% m/m**, um dado muito forte, mas que não apresenta
grandes ameaças pela sua tendência historicamente mais baixa.
Por fim, os números são mistos, **pois ainda que a leitura tenha sido em linha com as expectativas**, uma
variação mensal de 0,33% é **muito acima da meta do FED**. Além disso, o consumo pessoal apresentou
retração de 0,2%, o que alimenta a narrativa de estagflação
]

-> dados que você deverá tratar:
{texto}

"""

    resposta = openai.Client().chat.completions.create(

        model="gpt-4o-2024-08-06",
        messages=[{"role":"system", "content": "Você é um analista econômico"},
                  {"role": "user", "content": prompt}],
        temperature=0.7
        
    )

    hoje = datetime.date.today().strftime("%Y-%m-%d")
    with open("datasets/last_update.txt", "w", encoding="utf-8") as f:
        f.write(hoje)
    return resposta.choices[0].message.content
    

