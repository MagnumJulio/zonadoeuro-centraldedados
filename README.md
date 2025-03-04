# Dashboard Econômico

Este é um dashboard econômico que consome dados da API da Eurostat, Investing, Yahoo Finance e outros

## Funcionalidades

- Extração de séries históricas diretamente do **Investing.com** (ex: Confiança do Consumidor, Encomendas à Indústria Alemã).
- Flexibilidade para adicionar novos indicadores e ajustar parâmetros específicos por série.
- Gráficos de evolução temporal interativos.
- Filtros dinâmicos por país, parceiro comercial, ou qualquer outra dimensão disponível.
- Comparação direta entre valores realizados e previsões (Actual vs Forecast).
- Geração de comentários automáticos utilizando **OpenAI API**.
- Comentários salvos junto com os dados históricos para contextualizar cada atualização.
- Dashboard completo em **Streamlit**, com abas organizadas por tema e subtema.
- Opção para **download de dados filtrados** ou completos.
- Histórico de atualizações registrado.

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

- No Streamlit Cloud, sua chave da OpenAI ficará salva nas **secrets da plataforma**, e nunca no código.