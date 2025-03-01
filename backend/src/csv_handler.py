import csv

def dict_list_to_csv(dict_list, file_name, exclude_fields=None):
    """
    Transforma uma lista de dicionários em um arquivo CSV, permitindo a exclusão de campos específicos.

    Args:
        dict_list (list): Lista de dicionários.
        file_name (str): Nome do arquivo CSV a ser criado.
        exclude_fields (list, optional): Lista de campos a serem excluídos do CSV. Padrão é None.

    Returns:
        None
    """
    # Verifica se a lista não está vazia
    if not dict_list:
        raise ValueError("A lista de dicionários está vazia.")
    
    # Se exclude_fields não for fornecido, define como uma lista vazia
    exclude_fields = set(exclude_fields) if exclude_fields else set()

    # Obtém os cabeçalhos do CSV, excluindo os campos especificados
    headers = [key for key in dict_list[0].keys() if key not in exclude_fields]

    # Cria e escreve o arquivo CSV
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Escreve os cabeçalhos
        writer.writeheader()

        # Escreve os dados, excluindo os campos especificados
        for row in dict_list:
            filtered_row = {key: value for key, value in row.items() if key not in exclude_fields}
            writer.writerow(filtered_row)
    
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