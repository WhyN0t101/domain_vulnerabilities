import json

def ordenar_cidades(input_file, output_file):
    # Abrir o arquivo JSON de entrada
    with open(input_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)

    # Organizar o dicionário por ordem alfabética das chaves
    cidades_ordenadas = dict(sorted(cidades.items()))

    # Escrever o dicionário ordenado no arquivo JSON de saída
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cidades_ordenadas, f, ensure_ascii=False, indent=4)

# Exemplo de uso
input_file = 'cidades_input.json'  # Caminho para o arquivo de entrada
output_file = 'cidades_ordenadas.json'  # Caminho para o arquivo de saída

ordenar_cidades(input_file, output_file)
