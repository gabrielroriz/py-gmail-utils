from google_apis import init_gmail_service, get_email_messages, get_email_message_details, add_label_to_email, list_labels, archive_email, create_label
from csv_handler import dict_list_to_csv, csv_to_dict
import re
from collections import Counter

def extract_email_domain(text):
    """
    Extrai o domínio (parte após o @, incluindo o @) de um e-mail presente na string.
    
    :param text: String que contém o e-mail dentro de "<>".
    :return: O domínio do e-mail (incluindo o @) ou None se não for encontrado.
    """
    email_regex = r"<([^>]+)>"
    match = re.search(email_regex, text, re.IGNORECASE)  
    
    if match:
        email = match.group(1)  # Extrai o e-mail completo
        at_domain = email[email.index('@'):]  # Pega o @ e o que vem depois
        return at_domain
    return None

def extract_email(text):
    """
    Extrai o e-mail de uma string no formato "Texto <email@example.com>".
    
    :param text: String que contém o e-mail dentro de "<>".
    :return: O e-mail extraído ou None se não for encontrado.
    """
    email_regex = r"<([^>]+)>"
    match = re.search(email_regex, text, re.IGNORECASE)
    return match.group(1) if match else None

def find_labels_by_name(labels, name):
    for label in labels:
        if label['name'] == name:
            return label
            
    return None

def domain_frequency(array_of_dicts, key):
    """
    Calcula a frequência dos domínios de e-mail em um array de dicionários.
    
    :param array_of_dicts: Lista de dicionários.
    :param key: Chave onde o e-mail está armazenado nos dicionários.
    :return: Um dicionário com os domínios como chaves e suas frequências como valores.
    """
    domains = []
    
    for item in array_of_dicts:
        if key in item:  # Verifica se a chave existe no dicionário
            domain = extract_email_domain(item[key])
            if domain:
                domains.append(domain)
    
    # Calcula a frequência dos domínios
    return dict(Counter(domains))

RULES = {
    'Brasil Paralelo': {
        'domains': ['@brasilparalelo.com.br', "@email.brasilparalelo.com.br"],
        'archive': True
    },
    'Italo Marsili': {
        'domains': ['@italomarsili.com.br'],
        'archive': True
    },
    'ClickUp':{
        'domains': ['@tasks.clickup.com'],
        'archive': True
    }
}

FROM_CLOUD = True
CSV_SAVE = False
MAX_RESULTS = 200

# Init

client_secret_file = 'client_secret.json'
service = init_gmail_service(client_secret_file)

# Labels

labels = list_labels(service)

# Messages List
if FROM_CLOUD:
    messages_list = get_email_messages(service, max_results=MAX_RESULTS)
else:
    messages_list = csv_to_dict("./emails.csv")

# Message Details
if FROM_CLOUD:
    details_list = []
    for i, msg in enumerate(messages_list):
        details = get_email_message_details(service, msg['id'])
        details_list.append(details)
        # Calcula a porcentagem e printa
        percentage = ((i + 1) / len(messages_list)) * 100
        print(f"Progress: {percentage:.2f}%")

    if CSV_SAVE:
        dict_list_to_csv(details_list, "emails.csv")

# exit()

# Run rules
for label_string in RULES:
        rule_domains = RULES[label_string]["domains"]
        rule_acrhive = RULES[label_string]["archive"]
        label = find_labels_by_name(labels, label_string)

        # Find the message that matches the rule.
        for message in details_list:
            domain = extract_email_domain(message['sender']) # Extract @something.com.br
            if domain in rule_domains: # Match
                print(message)
                if label["id"] != None:
                    add_label_to_email(service, message["id"], label["id"])
                else:
                    label = create_label(service, label_string)
                    add_label_to_email(service, message["id"], label["id"])

                if rule_acrhive:
                    archive_email(service, message["id"])

   
# print(messages[0])
# print(find_labels_by_name(labels, "Teste")["id"])

# archive_email(service, messages[0]["id"])
# add_label_to_email(service, messages[0]["id"], find_labels_by_name(labels, "Teste")["id"])

# details_list = []



# 






# Actions!
# fr = domain_frequency(messages, "sender")
# print(fr)