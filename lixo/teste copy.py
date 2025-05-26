import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

paleta_cores = ["#000000", "#082631", "#166083", "#37A6D9", "#AFABAB", "#82C1DB"]

# Carregar os dados
file_path = "dados_deflacionados_final.xlsx"

# Importação e exportação
df_import = pd.read_excel(file_path, sheet_name="realimp")
df_export = pd.read_excel(file_path, sheet_name="realexp")

# PIB real deflacionado
df_pib = pd.read_excel(file_path, sheet_name="pibreal")

# Garantir que o ano seja interpretado corretamente como número
df_import["Period"] = pd.to_numeric(df_import["Period"], errors="coerce")
df_export["Period"] = pd.to_numeric(df_export["Period"], errors="coerce")
df_pib["Year"] = pd.to_numeric(df_pib["Year"], errors="coerce")

# Mesclar os dados com o PIB real deflacionado
df_import = df_import.merge(df_pib[["Year", "PIB_Real"]], left_on="Period", right_on="Year", how="left")
df_export = df_export.merge(df_pib[["Year", "PIB_Real"]], left_on="Period", right_on="Year", how="left")

# Excluir a coluna duplicada de ano
df_import.drop(columns=["Year"], inplace=True)
df_export.drop(columns=["Year"], inplace=True)

# Criar DataFrame final para o gráfico
df_trade = df_import[["Period"]].copy()

# Identificar categorias de produtos, excluindo colunas desnecessárias
categorias = [col for col in df_import.columns if col not in ["Period", "Total Census Basis (1)", "PIB_Real", "Residual (3)"]]

# Importações entram NEGATIVAS, Exportações entram POSITIVAS
for categoria in categorias:
    df_trade[categoria] = -df_import[categoria] / df_import["PIB_Real"]  # Importações negativas
    df_trade[categoria] += df_export[categoria] / df_export["PIB_Real"]  # Exportações positivas

# Criar gráfico de barras empilhadas com a nova paleta de cores
fig, ax = plt.subplots(figsize=(12, 6))

df_trade.set_index("Period").plot(
    kind="bar", stacked=True, ax=ax, color=paleta_cores, width=0.8
)

# Ajustar formato do eixo Y para porcentagem
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))

# Ajustes visuais
ax.set_title("Trade Balance as a Proportion of GDP", fontsize=14, fontweight="bold", color="#082631")
ax.set_xlabel("Year", fontsize=12, color="#082631")
ax.set_ylabel("Percentage of GDP", fontsize=12, color="#082631")
ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=10, labelcolor="#082631")
plt.xticks(rotation=45, ha="right", color="#082631")
plt.yticks(color="#082631")
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.5, color="#AFABAB")

# Exibir gráfico
plt.show()