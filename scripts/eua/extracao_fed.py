import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import seaborn as sns

# Substitua pela sua chave da API do BEA
BEA_API_KEY = 'F4F690A9-5029-4D9C-A8AE-D323ACE093A0'

# Função para buscar dados do BEA
def get_bea_data(table, industry_code):
    """ Obtém dados do PIB por setor da API do BEA """
    url = f'https://apps.bea.gov/api/data/?UserID={BEA_API_KEY}&method=GetData&datasetname=GDPbyIndustry&TableName={table}&Frequency=Q&Year=ALL&Industry=ALL&TableID=ALL&ResultFormat=json'
    
    response = requests.get(url)
    data = response.json()

    # Exibir estrutura da resposta para debug
    if 'BEAAPI' not in data or 'Results' not in data['BEAAPI'] or 'Data' not in data['BEAAPI']['Results']:
        raise ValueError(f"Erro na resposta da API: {data}")

    # Transformar em DataFrame
    df = pd.DataFrame(data['BEAAPI']['Results']['Data'])

    # Filtrar a indústria desejada
    df = df[df['Industry'] == industry_code]  # O campo correto é 'Industry', não 'LineNumber'

    # Converter para formato numérico
    df['TimePeriod'] = pd.to_datetime(df['TimePeriod'])
    df['DataValue'] = df['DataValue'].astype(float)

    return df[['TimePeriod', 'DataValue']].set_index('TimePeriod')


# PIB Total (Todos os setores combinados)
pib_total = get_bea_data('T10106', 'II')  # "II" = All Industries

# PIB da Indústria
pib_industria = get_bea_data('T10106', '31G')  # "31G" = Manufacturing (Manufatura)

# PIB de Serviços
pib_servicos = get_bea_data('T10106', 'PSERV')  # "PSERV" = Private Services-Producing Industries

# PIB de Construção
pib_construcao = get_bea_data('T10106', '23')  # "23" = Construction

# Criando DataFrame Consolidado
df = pd.concat([pib_total, pib_industria, pib_servicos, pib_construcao], axis=1)
df.columns = ['PIB Total', 'PIB Indústria', 'PIB Serviços', 'PIB Construção']

# Exibir os primeiros valores
print(df.head())

# # Normalizando os dados (Índice 100 no início de cada recessão)
# recession_periods = [
#     ('2001-03-01', '2001-11-01'),
#     ('2007-12-01', '2009-06-01'),
#     ('2020-02-01', '2020-04-01')
# ]

# fig, ax1 = plt.subplots(figsize=(10, 5))
# ax2 = ax1.twinx()  # Criando eixo secundário

# # Plotando PIB Total e Indústria
# sns.lineplot(data=df, x=df.index, y='PIB Total', label='PIB Total', ax=ax1, color='b')
# sns.lineplot(data=df, x=df.index, y='PIB Indústria', label='PIB Indústria', ax=ax1, color='g')
# ax1.set_ylabel('PIB Total e Indústria (Base 100)', color='b')

# # Plotando PIB de Serviços no eixo secundário
# sns.lineplot(data=df, x=df.index, y='PIB Serviços', label='PIB Serviços', ax=ax2, color='r')
# ax2.set_ylabel('PIB Serviços (Base 100)', color='r')

# # Destacando recessões
# for start, end in recession_periods:
#     ax1.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.3)

# # Configuração do gráfico
# ax1.set_title('Comportamento do PIB por Setor em Recessões')
# ax1.set_xlabel('Ano')
# ax1.xaxis.set_major_locator(mdates.YearLocator(5))
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# plt.xticks(rotation=45)
# ax1.grid()
# ax1.legend(loc='upper left')
# ax2.legend(loc='upper right')

# plt.show()






# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns
# from fredapi import Fred

# # Substitua pela sua chave da API do FRED
# fred = Fred(api_key='072da8f2a03814a61c76e1cb34dcf3ad')

# # Baixando dados do PIB real total e do PIB da manufatura (séries do FRED)
# pib_total = fred.get_series('GDPC1')  # PIB real dos EUA
# pib_manufatura = fred.get_series('IPMAN')  # Produção industrial na manufatura como proxy

# # Convertendo para DataFrame
# df = pd.DataFrame({'PIB Total': pib_total, 'PIB Manufatura': pib_manufatura})
# df = df.dropna()

# # Normalizando os dados (Índice 100 no início de cada recessão)
# recession_periods = [
#     ('2001-03-01', '2001-11-01'),
#     ('2007-12-01', '2009-06-01'),
#     ('2020-02-01', '2020-04-01')
# ]

# fig, ax1 = plt.subplots(figsize=(10, 5))
# ax2 = ax1.twinx()  # Criando eixo secundário

# # Plotando PIB Total no eixo primário
# sns.lineplot(data=df, x=df.index, y='PIB Total', label='PIB Total', ax=ax1, color='b')
# ax1.set_ylabel('PIB Total (Base 100)', color='b')

# # Plotando PIB da Manufatura no eixo secundário
# sns.lineplot(data=df, x=df.index, y='PIB Manufatura', label='PIB Manufatura', ax=ax2, color='r')
# ax2.set_ylabel('Produção Industrial (Base 100)', color='r')

# # Destacando recessões
# for start, end in recession_periods:
#     ax1.axvspan(pd.to_datetime(start), pd.to_datetime(end), color='gray', alpha=0.3)

# # Configuração do gráfico
# ax1.set_title('Comportamento do PIB Total vs. PIB da Manufatura em Recessões')
# ax1.set_xlabel('Ano')
# ax1.xaxis.set_major_locator(mdates.YearLocator(5))
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# plt.xticks(rotation=45)
# ax1.grid()
# ax1.legend(loc='upper left')
# ax2.legend(loc='upper right')

# plt.show()
