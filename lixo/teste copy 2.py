import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 📌 1. Carregar o deflator do PIB
df_deflator = pd.read_excel("GDPDEF.xlsx", parse_dates=["Year"])

# Converter para ano e extrair o último valor de cada ano
df_deflator["Year"] = df_deflator["Year"].dt.year
df_deflator = df_deflator.groupby("Year").last().reset_index()

# Renomear a coluna do deflator para garantir consistência
df_deflator.rename(columns={"Ano": "Year", "Deflator": "GDPDEF"}, inplace=True)

# 📌 2. Carregar os dados do PIB nominal (incluindo manufatura e subsetores)
df_gdp = pd.read_excel("subsetores.xlsx")

# Remover duplicatas nos dados do PIB antes de mesclar
df_gdp = df_gdp.drop_duplicates(subset=["Year"])

# Mesclar os dados pelo ano
df = pd.merge(df_gdp, df_deflator, on="Year", how="left")

# Remover possíveis duplicatas após a mesclagem
df = df.drop_duplicates(subset=["Year"])

# 📌 3. Lista das colunas a serem deflacionadas (excluindo "Year" e "GDPDEF")
colunas_pib = [col for col in df.columns if col not in ["Year", "GDPDEF"]]

# 📌 4. Aplicar a deflação: PIB Real = PIB Nominal / (Deflator / 100)
for col in colunas_pib:
    df[f"{col}_Real"] = df[col] / (df["GDPDEF"] / 100)

# 📌 5. Criar macrogrupos agregados
df["Bens de Capital"] = (
    df["Machinery_Real"] + 
    df["Computer and electronic products_Real"] +
    df["Electrical equipment, appliances, and components_Real"]
)

df["Bens de Consumo Duráveis"] = (
    df["Motor vehicles, bodies and trailers, and parts_Real"] + 
    df["Furniture and related products_Real"] + 
    df["Wood products_Real"]
)

df["Bens de Consumo Não Duráveis"] = (
    df["Food and beverage and tobacco products_Real"] + 
    df["Paper products_Real"] +
    df["Textile mills and textile product mills_Real"] + 
    df["Apparel and leather and allied products_Real"]
)

df["Indústrias Químicas e Energéticas"] = (
    df["Chemical products_Real"] + 
    df["Plastics and rubber products_Real"] + 
    df["Petroleum and coal products_Real"]
)

# 📌 6. Calcular a participação das categorias agregadas no PIB total
colunas_macro = ["Bens de Capital", "Bens de Consumo Duráveis", "Bens de Consumo Não Duráveis", "Indústrias Químicas e Energéticas"]

for col in colunas_macro:
    df[f"{col}_Share"] = df[col] / df["All industries_Real"]

# 📌 7. Criar gráfico de colunas empilhadas com macrogrupos
fig, ax = plt.subplots(figsize=(12, 6))

# Criar DataFrame apenas com os grupos agregados
df_share = df[["Year"] + [col + "_Share" for col in colunas_macro]]

# Ordenar os anos para evitar duplicação
df_share = df_share.sort_values("Year").set_index("Year")

# Plotar gráfico de colunas empilhadas
df_share.plot(
    kind="bar", stacked=True, color=["#082631", "#166083", "#37A6D9", "#AFABAB", "#82C1DB"], width=0.8, ax=ax
)

# Formatar eixo Y como porcentagem
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

# Ajustes visuais
ax.set_title("Participação dos Macrogrupos da Manufatura no PIB Total", fontsize=14, fontweight="bold", color="#082631")
ax.set_xlabel("Ano", fontsize=12, color="#082631")
ax.set_ylabel("Participação no PIB (%)", fontsize=12, color="#082631")
ax.legend(title="Macrogrupos", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=10, labelcolor="#082631")
plt.xticks(rotation=45, ha="right", color="#082631")
plt.yticks(color="#082631")
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.5, color="#AFABAB")

# Exibir gráfico
plt.show()

# 📌 8. Salvar os dados atualizados
df.to_excel("dados_deflacionados.xlsx", index=False)

# Exibir as primeiras linhas para conferência
print(df.head())
