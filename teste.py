import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Carregar os dados
file_path = "dados_finais.xlsx"
df = pd.read_excel(file_path)

# Garantir que o ano seja interpretado corretamente como número
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Carregar as datas de recessão dos EUA (fonte: NBER)
recession_periods = [(1990, 1991),
    (2000, 2001), (2007, 2009), (2019, 2020)
]

# Criar a figura e os eixos
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar as séries normalizadas
ax.plot(df["Year"], df["All_industries_Real_Normalizado"], label="All Industries", color="blue")
ax.plot(df["Year"], df["Manufacturing_Real_Normalizado"], label="Manufacturing + Mining", color="red")

# Destacar períodos recessivos
for start, end in recession_periods:
    ax.axvspan(start, end, color="gray", alpha=0.3)

# Customizações do gráfico
ax.set_title("Real GDP by Industry (Normalized, 1987=1)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

# Exibir gráfico
plt.show()
