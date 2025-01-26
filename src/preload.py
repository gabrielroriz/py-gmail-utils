from src.google_apis import GmailAPI

from src.csv_handler import dict_list_to_csv, csv_to_dict

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

def string_percentage(current, totalSize):
        percentage = ((current + 1) / totalSize) * 100
        return f"{percentage:.2f}%"

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
    }, 
    'ByteByteGo': {
        'domains': ['bytebytego@substack.com'],
        'archive': True
    },
    'Mercado Livre': {
        'domains': ['@a.mercadolivre.com.br', '@r.mercadolivre.com.br'],
        'archive': True
    }, 
    'CLC': {
        'domains': ['@literaturaclassica.com.br'],
        'archive': True
    },
    'CitizenGo': {
        'domains': ['@citizengo.org'],
        'archive': True
    }
}


LOAD_FROM_CLOUD = True
SAVE_DATA_CSV = False
MAX_RESULTS = 10

# Init
gmail_api = GmailAPI('client_secret.json')

# Labels
labels = gmail_api.list_labels()

# Messages List
if LOAD_FROM_CLOUD:
    mail_list = gmail_api.get_mail_list(max_results=MAX_RESULTS)
else:
    mail_list = csv_to_dict("./data/emails.csv")

# Message Content
if LOAD_FROM_CLOUD:
    mail_list_fullcontent = []
    for i, msg in enumerate(mail_list):
        details = gmail_api.get_mail_content(msg['id']) # Get mail content
        mail_list_fullcontent.append(details) # Append result to the array
        print(f"Progress: {string_percentage(i, len(mail_list))}% | {extract_email(details['sender'])} / {details['subject']} / {msg['id']}") # Print progress

    if SAVE_DATA_CSV:
        dict_list_to_csv(mail_list_fullcontent, "data/emails.csv")

#Rules
for label_string in RULES:
        rule_domains = RULES[label_string]["domains"]
        rule_acrhive = RULES[label_string]["archive"]
        label = find_labels_by_name(labels, label_string)

        # Find the message that matches the rule.
        for message in mail_list_fullcontent:
            domain = extract_email_domain(message['sender']) # Extract @something.com.br
            if domain in rule_domains: # Match
                if label is not None and "id" in label:
                    gmail_api.add_label_to_email(message["id"], label["id"])
                    print(f"Marcador '{label_string}' adicionado ao e-mail: {extract_email(message['sender'])} / {message['subject']} / {message['id']}")

                else:
                    label = gmail_api.create_label(label_string)
                    print(f"Marcador '{label_string}' criado com sucesso")

                    gmail_api.add_label_to_email(message["id"], label["id"])
                    print(f"Marcador '{label_string}' adicionado ao e-mail: {extract_email(message['sender'])} / {message['subject']} / {message['id']}")

                if rule_acrhive:
                    gmail_api.archive_email(message["id"])







# # Actions!
# # fr = domain_frequency(messages, "sender")
# # print(fr)