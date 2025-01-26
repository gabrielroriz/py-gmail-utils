import csv

def dict_list_to_csv(dict_list, file_name):
    """
    Transforma uma lista de dicionários em um arquivo CSV.

    Args:
        dict_list (list): Lista de dicionários.
        file_name (str): Nome do arquivo CSV a ser criado.

    Returns:
        None
    """
    # Verifica se a lista não está vazia
    if not dict_list:
        raise ValueError("A lista de dicionários está vazia.")

    # Obtém os cabeçalhos do CSV das chaves do primeiro dicionário
    headers = dict_list[0].keys()

    # Cria e escreve o arquivo CSV
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Escreve os cabeçalhos
        writer.writeheader()

        # Escreve os dados
        for row in dict_list:
            writer.writerow(row)

    print(f"Arquivo CSV '{file_name}' criado com sucesso!")

def csv_to_dict(csv_file_path):
    try:
        # Abrir o arquivo CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            # Ler o conteúdo do CSV como um dicionário
            csv_reader = csv.DictReader(csv_file)

            # Converter o conteúdo para uma lista de dicionários
            data = [row for row in csv_reader]

        # Retornar a lista de dicionários
        return data

    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None