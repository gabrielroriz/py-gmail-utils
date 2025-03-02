from google_apis import GmailAPI, gmail_get_label_by_name, gmail_get_email, gmail_get_email_domain

from multiprocessing import Pool

from csv_handler import dict_list_to_csv, csv_to_dict

import re

from collections import Counter

import os

import sys

import time

from tqdm import tqdm

from collections import Counter

def frequency_analysis(data, field_name):
    # Contar a ocorrência dos valores do campo especificado

    field_values = [item[field_name] for item in data if field_name in item]
    field_values = [gmail_get_email_domain(field_value) for field_value in field_values] # Only @something.com.br

    counts = Counter(field_values)

    # Calcular o total de ocorrências
    total = sum(counts.values())
    
    # Criar a lista de resultados em ordem decrescente de frequência
    result = sorted([
        {
            "name": name,
            "frequency": count,
            "percentage": f"{(count / total) * 100:.0f}%"
        }
        for name, count in counts.items()
    ], key=lambda x: x["frequency"], reverse=True)
    
    return result


def string_percentage(current, totalSize):
        percentage = ((current + 1) / totalSize) * 100
        return f"{percentage:.2f}%"

RULES = {
    # 'Brasil Paralelo': {
    #     'domains': ['@brasilparalelo.com.br', "@email.brasilparalelo.com.br"],
    #     'archive': True
    # },
    # 'Italo Marsili': {
    #     'domains': ['@italomarsili.com.br'],
    #     'archive': True
    # },
    # 'ClickUp':{
    #     'domains': ['@tasks.clickup.com'],
    #     'archive': True
    # }, 
    # 'ByteByteGo': {
    #     'domains': ['@substack.com'],
    #     'archive': True
    # },
    # 'Mercado Livre': {
    #     'domains': ['@a.mercadolivre.com.br', '@r.mercadolivre.com.br'],
    #     'archive': True
    # }, 
    # 'CLC': {
    #     'domains': ['@literaturaclassica.com.br'],
    #     'archive': True
    # },
    # 'CitizenGo': {
    #     'domains': ['@citizengo.org'],
    #     'archive': True
    # },
    "Experts In": {
        'domains': ['@orodrigogurgel.com.br'],
        'archive': True
    }
}


LOAD_FROM_CLOUD = False
SAVE_DATA_CSV = False
SAVE_FREQUENCY = False

def init_gmail_api():
    global gmail_api
    gmail_api = GmailAPI('client_secret.json')
        
def get_mail_content(msg):    
    return gmail_api.get_mail_content(msg['id'])

# labels = gmail_api.list_labels()

def get_mail(max_results = 1000, from_cloud=True, csv_persist=False, request=None):

    # Get mail list (without content)
    if from_cloud:
        init_gmail_api()
        mail_list = gmail_api.get_mail_list(max_results=max_results)
    else:
        mail_list = csv_to_dict("./data/emails.csv")

    # For each item, get mail content.
    if from_cloud:
        # Start time counting.
        start_parallel = time.perf_counter() 
        
        # Get each content mail with parallel execution.
        with Pool(processes=os.cpu_count(), initializer=init_gmail_api) as pool:
            mail_list_fullcontent = list(
                tqdm(
                    pool.imap(get_mail_content, mail_list), 
                    total=len(mail_list), 
                    desc="Processando e-mails"
                )
            )

        # End time counting
        end_parallel = time.perf_counter()
        print(f"Tempo total: {end_parallel - start_parallel:.4f} segundos")

        if csv_persist:
            dict_list_to_csv(mail_list_fullcontent, "data/emails.csv", ["body"])
    else:
        mail_list_fullcontent = mail_list

    return mail_list_fullcontent


# if SAVE_FREQUENCY:
#     frequency = frequency_analysis(mail_list_fullcontent, "sender")
#     dict_list_to_csv(frequency, "data/fr.csv")




# sys.exit(0)
#########
# RULES #
#########
# for label_string in RULES:
#         rule_domains = RULES[label_string]["domains"]
#         rule_acrhive = RULES[label_string]["archive"]
#         label = gmail_get_label_by_name(labels, label_string)

#         # Find the message that matches the rule.
#         for message in mail_list_fullcontent:
#             domain = gmail_get_email_domain(message['sender']) # Extract @something.com.br
#             if domain in rule_domains: # Match
                # if label is not None and "id" in label:
                #     gmail_api.add_label_to_email(message["id"], label["id"])
                #     print(f"Marcador '{label_string}' adicionado ao e-mail: {gmail_get_email(message['sender'])} / {message['subject']} / {message['id']}")

                # else:
                #     label = gmail_api.create_label(label_string)
                #     print(f"Marcador '{label_string}' criado com sucesso")

                #     gmail_api.add_label_to_email(message["id"], label["id"])
                #     print(f"Marcador '{label_string}' adicionado ao e-mail: {gmail_get_email(message['sender'])} / {message['subject']} / {message['id']}")

                # if rule_acrhive:
                    # gmail_api.archive_email(message["id"])







# # Actions!
# # fr = domain_frequency(messages, "sender")
# # print(fr)