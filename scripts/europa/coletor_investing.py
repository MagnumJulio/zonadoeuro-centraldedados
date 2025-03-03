import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def iniciar_driver(headless=True):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extrair_tabela_investing(url, tema, subtema, pasta_base="datasets"):
    driver = iniciar_driver(headless=True)

    print(f"Acessando: {url}")
    driver.get(url)

    # Espera carregar a página (ajuste conforme a lentidão do site ou da conexão)
    time.sleep(5)

    # Captura o HTML após o carregamento completo
    html = driver.page_source
    driver.quit()

    # Parseia com BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find("table", {"class": "genTbl closedTbl historicalTbl"})

    if not tabela:
        raise ValueError("Tabela de histórico não encontrada. Verifique a estrutura da página.")

    # Extrai as linhas
    linhas = tabela.find_all("tr")[1:]

    dados = []
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) < 5:
            continue

        data = colunas[0].text.strip()
        valor = colunas[1].text.strip().replace(",", "")
        dados.append([data, valor])

    df = pd.DataFrame(dados, columns=['time', 'value'])

    # Prepara os diretórios
    tema_path = os.path.join(pasta_base, tema)
    os.makedirs(tema_path, exist_ok=True)

    arquivo_csv = os.path.join(tema_path, f"{subtema}_historico.csv")
    df.to_csv(arquivo_csv, index=False)

    print(f"Dados salvos em: {arquivo_csv}")

    return df

# Exemplo de uso
if __name__ == "__main__":
    url = "https://br.investing.com/economic-calendar/inflation-rate-810"  # Troque para a URL real
    extrair_tabela_investing(url, tema="inflacao", subtema="ipc")
