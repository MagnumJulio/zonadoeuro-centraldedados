# Dashboard Econômico - Produção Industrial Eurostat

Este é um dashboard econômico que consome dados da API da Eurostat, focado na produção industrial.

## Funcionalidades

- Insira o link da API diretamente no dashboard.
- Visualize os dados brutos.
- Veja estatísticas descritivas.
- Acompanhe gráficos simples de evolução.

## Como rodar localmente

1. Clone o repositório.
2. Crie `.streamlit/secrets.toml` com sua chave de API.
3. Instale os pacotes:

    ```
    pip install -r requirements.txt
    ```

4. Rode:

    ```
    streamlit run app.py
    ```

## Sobre o Streamlit Cloud

- No Streamlit Cloud, sua chave ficará salva nas **secrets da plataforma**, e nunca no código.