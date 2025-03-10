import pdfplumber
from redlines import Redlines
import markdown2

def extrair_texto_pdf(caminho_pdf):
    texto = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto.append(texto_pagina)
    return "\n".join(texto)

def juntar_linhas_quebradas(texto):
    linhas = texto.split("\n")
    linhas_corrigidas = []
    buffer = []

    for linha in linhas:
        linha = linha.strip()
        if linha:
            buffer.append(linha)
            if linha[-1] in ".!?":  # Final de parágrafo
                linhas_corrigidas.append(" ".join(buffer))
                buffer = []

    if buffer:
        linhas_corrigidas.append(" ".join(buffer))

    return "\n\n".join(linhas_corrigidas)

# Caminhos dos arquivos PDF
pdf_original = 'scripts\Monetary policy decisions30jan.pdf'
pdf_revisado = 'scripts\Monetary policy decisions6mar.pdf'

# Extração e limpeza de texto
texto_original = juntar_linhas_quebradas(extrair_texto_pdf(pdf_original))
texto_revisado = juntar_linhas_quebradas(extrair_texto_pdf(pdf_revisado))

# Comparação com Redlines
comparador = Redlines(texto_original, texto_revisado)

# Converte o resultado Markdown para HTML
html_diferencas = markdown2.markdown(comparador.output_markdown)

# CSS Personalizado
css_personalizado = """
<style>
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 20px;
}
del {
    color: red;
}
ins {
    color: #166083;
    font-weight: bold;
    text-decoration: none;
}
</style>
"""

# Gera o HTML Final
html_personalizado = f"""
<html>
<head>
    <title>Comparação de Documentos PDF</title>
    {css_personalizado}
</head>
<body>
    <h1>Comparação de Documentos PDF</h1>
    {html_diferencas}
</body>
</html>
"""

# Salva em arquivo
with open('comparacao_personalizada.html', 'w', encoding='utf-8') as f:
    f.write(html_personalizado)

print("Comparação concluída! Verifique o arquivo 'comparacao_personalizada.html'.")
