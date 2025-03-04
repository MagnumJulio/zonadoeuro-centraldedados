import os
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import random
from time import sleep
import re


def atualizar_last_update(tema, subtema, pasta_base="datasets"):
    """Atualiza o arquivo last_update.txt com a última data de atualização."""
    arquivo_last_update = os.path.join(pasta_base, "last_update.txt")
    data_atualizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(arquivo_last_update, "a", encoding="utf-8") as f:
        f.write(f"{tema}/{subtema} atualizado em {data_atualizacao}\n")

    print(f"🕒 Última atualização registrada em {arquivo_last_update}")


def converter_data_flex(release_date_str):
    """
    Converte diretamente a data de publicação para o formato 'yyyy-mm-dd',
    ignorando qualquer mês entre parênteses.

    Exemplos:
    - '07.03.2025 (Jan)' → '2025-03-07'
    - '06.07.2017 (Mai)' → '2017-07-06'
    - 'Mar 21, 2025 (Mar)' → '2025-03-21'
    """

    meses_abreviados = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
        "Fev": "02", "Abr": "04", "Mai": "05", "Ago": "08",
        "Set": "09", "Out": "10", "Dez": "12"
    }

    release_date_str = ' '.join(release_date_str.split())

    try:
        # Caso 1 - Formato europeu '07.03.2025 (Jan)'
        match_europeu = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", release_date_str)
        if match_europeu:
            dia, mes, ano = match_europeu.groups()
            return f"{ano}-{mes}-{dia}"

        # Caso 2 - Formato americano 'Mar 21, 2025'
        match_americano = re.match(r"(\w{3}) (\d{1,2}), (\d{4})", release_date_str)
        if match_americano:
            mes_str, dia, ano = match_americano.groups()
            mes = meses_abreviados.get(mes_str)

            if not mes:
                raise ValueError(f"❌ Mês abreviado '{mes_str}' não reconhecido.")

            return f"{ano}-{mes}-{int(dia):02d}"

        raise ValueError(f"❌ Formato de data não reconhecido: '{release_date_str}'")

    except Exception as e:
        print(f"❌ Erro ao converter data de publicação '{release_date_str}': {e}")
        return None


def extrair_tabela_investing(url, tema, subtema, pasta_base="datasets"):
    evento_id = url.split("-")[-1]
    xpath_tabela = f'//*[@id="eventHistoryTable{evento_id}"]'
    xpath_show_more = f'//*[@id="showMoreHistory{evento_id}"]/a'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        print(f"🌍 Acessando: {url}")

        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
        except PlaywrightTimeoutError:
            print("❌ Timeout ao carregar a página.")
            browser.close()
            return None

        try:
            page.locator("#onetrust-accept-btn-handler").click(timeout=5000)
            print("🍪 Cookies aceitos!")
        except PlaywrightTimeoutError:
            print("✅ Nenhum pop-up de cookies encontrado.")

        for i in range(15):
            rnumber = random.randint(4, 9)
            try:
                show_more_button = page.locator(f'xpath={xpath_show_more}')
                if show_more_button.is_visible():
                    show_more_button.click()
                    sleep(rnumber)
                    print(f"🔄 Show more clicado ({i+1}/15)")
                    page.wait_for_timeout(1500)
                else:
                    print("✅ Botão 'Show more' não visível, seguindo...")
                    break
            except Exception as e:
                print(f"⚠️ Erro ao clicar em 'Show more': {e}")
                break

        try:
            page.wait_for_selector(f'xpath={xpath_tabela}', timeout=15000)
        except PlaywrightTimeoutError:
            print("❌ Tabela não carregou após os cliques.")
            browser.close()
            return None

        tabela_html = page.locator(f'xpath={xpath_tabela}').inner_html()
        browser.close()

    soup = BeautifulSoup(tabela_html, "html.parser")
    linhas = soup.find_all("tr")[1:]

    dados = []
    for linha in linhas:
        colunas = linha.find_all("td")
        if len(colunas) < 4:
            continue

        release_date = colunas[0].text.strip()
        actual = colunas[2].text.strip()
        forecast = colunas[3].text.strip()

        data_formatada = converter_data_flex(release_date)

        if data_formatada:
            if actual:
                dados.append([data_formatada, 'actual', actual])
            if forecast:
                dados.append([data_formatada, 'forecast', forecast])

    df_novo = pd.DataFrame(dados, columns=['time', 'tipo', 'value'])

    df_novo['time'] = pd.to_datetime(df_novo['time'], errors='coerce').dt.date
    
    df_novo['value'] = (
        df_novo['value']
        .str.replace("−", "-", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .replace("-", pd.NA)
    )

    df_novo = df_novo.dropna()

    tema_path = os.path.join(pasta_base, tema)
    os.makedirs(tema_path, exist_ok=True)

    arquivo_csv = os.path.join(tema_path, f"{subtema}_historico.csv")

    if os.path.exists(arquivo_csv):
        df_antigo = pd.read_csv(arquivo_csv)
        df_antigo['time'] = pd.to_datetime(df_antigo['time'], errors='coerce').dt.date
        df = pd.concat([df_antigo, df_novo]).drop_duplicates(subset=['time', 'tipo'], keep='last').sort_values(by=['time', 'tipo'])
    else:
        df = df_novo

    df.to_csv(arquivo_csv, index=False)
    print(f"✅ Dados salvos em: {arquivo_csv}")

    atualizar_last_update(tema, subtema, pasta_base)

    return df
