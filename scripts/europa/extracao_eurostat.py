import requests
import pandas as pd
import itertools

def puxar_dados(url):
    # Puxar dados
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    dimensions = data['dimension']
    dimension_names = data['id']
    
    # Função para extrair categorias de uma dimensão
    def extract_categories(dimension):
        categories = list(dimension['category']['index'].keys())
        labels = dimension['category']['label']
        return categories, labels


    dimension_data = {}

    for dim in dimension_names:
        categories,labels = extract_categories(dimensions[dim])
        dimension_data[dim] = {
            'categories': categories,
            'labels': labels
        }


    index_ranges = [range(len(dimension_data[dim]['categories'])) for dim in dimension_names]
    index_combinations = list(itertools.product(*index_ranges))

    # Criar DataFrame com todas as combinações de labels
    rows = []
    for idx_comb in index_combinations:
        row = {}
        for i, dim in enumerate(dimension_names):
            category_key = dimension_data[dim]['categories'][idx_comb[i]]
            row[dim] = dimension_data[dim]['labels'][category_key]
        rows.append(row)


    df = pd.DataFrame(rows)

    # Preencher coluna "value" com os valores da Eurostat na ordem (None para buracos)
    values = []
    for idx in range(len(index_combinations)):
        values.append(data['value'].get(str(idx), None))

    df['value'] = values

    # Converter a coluna time para datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df['time'] = df['time'].dt.date

    return df


def salvar_comentario(topico,subtopico, texto):
    with open(f"D:/Impactus/Projetos-Impactus/pyimpactus/meu-dashboard1/meu-dashboard1/datasets/{topico}/{subtopico}_comentarios.md", "w", encoding="utf-8") as f:
        f.write(texto)


def salvar_base(topico,subtopico, df):
    df.to_csv(f"D:/Impactus/Projetos-Impactus/pyimpactus/meu-dashboard1/meu-dashboard1/datasets/{topico}/{subtopico}_historico.csv", index=False)

