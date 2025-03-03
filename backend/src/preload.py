from google_apis import GmailAPI, gmail_get_label_by_name, gmail_get_email, gmail_get_email_domain

from multiprocessing import Pool, Value

from csv_handler import dict_list_to_csv, csv_to_dict

import re

from collections import Counter

import os

import sys

import time

from tqdm import tqdm

from collections import Counter

from fastapi import Request

import asyncio

from utils import generate_csv_db_name

# RULES = {
#     # 'Brasil Paralelo': {
#     #     'domains': ['@brasilparalelo.com.br', "@email.brasilparalelo.com.br"],
#     #     'archive': True
#     # },
#     # 'Italo Marsili': {
#     #     'domains': ['@italomarsili.com.br'],
#     #     'archive': True
#     # },
#     # 'ClickUp':{
#     #     'domains': ['@tasks.clickup.com'],
#     #     'archive': True
#     # }, 
#     # 'ByteByteGo': {
#     #     'domains': ['@substack.com'],
#     #     'archive': True
#     # },
#     # 'Mercado Livre': {
#     #     'domains': ['@a.mercadolivre.com.br', '@r.mercadolivre.com.br'],
#     #     'archive': True
#     # }, 
#     # 'CLC': {
#     #     'domains': ['@literaturaclassica.com.br'],
#     #     'archive': True
#     # },
#     # 'CitizenGo': {
#     #     'domains': ['@citizengo.org'],
#     #     'archive': True
#     # },
#     "Experts In": {
#         'domains': ['@orodrigogurgel.com.br'],
#         'archive': True
#     }
# }

from google_apis import GmailAPI
from multiprocessing import Pool
from csv_handler import dict_list_to_csv, csv_to_dict
from fastapi import Request
import time
from tqdm import tqdm
import os
from typing import List, Dict, Any, Optional

# Configurações globais (podem ser movidas para um arquivo de configuração)
DEFAULT_MAX_RESULTS = 1000
CSV_EMAILS_DIR = "data/emails/"
CONTENT_FIELD = "body"

class GmailFetcher:
    """Classe para encapsular a lógica de busca de e-mails do Gmail."""

    def __init__(self):
        self.gmail_api = GmailAPI('client_secret.json')
    
    def _fetch_mail_list(self, max_results: int) -> List[Dict[str, Any]]:
        """Busca a lista de e-mails sem conteúdo."""
        return self.gmail_api.get_mail_list(max_results=max_results)

    def _get_mail_content(self, msg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Busca o conteúdo de um e-mail específico."""
        return self.gmail_api.get_mail_content(msg['id'])

    async def fetch_emails(
        self,
        request: Request,
        max_results: int = DEFAULT_MAX_RESULTS,
        from_cloud: bool = True,
        csv_persist: bool = False
    ) -> List[Dict[str, Any]]:
        
        # Obtém a lista de e-mails
        mail_list = (
            self._fetch_mail_list(max_results) 
            # if from_cloud else csv_to_dict(CSV_EMAILS_DIR)
        )

        if not from_cloud:
            return mail_list  # Retorna diretamente se não for do cloud

        # Processa os e-mails em paralelo / Calcula e exibe o tempo total
        start_time = time.perf_counter()
        mail_list_fullcontent = await self._process_emails_in_parallel(request, mail_list)
        end_time = time.perf_counter()
        print(f"Tempo total: {end_time - start_time:.4f} segundos")
        
        # Persiste em CSV, se solicitado
        if csv_persist:
            dict_list_to_csv(mail_list_fullcontent, f"{CSV_EMAILS_DIR}{generate_csv_db_name(len(mail_list_fullcontent))}.csv", [CONTENT_FIELD])

        return mail_list_fullcontent

    async def _process_emails_in_parallel(self, request: Request, mail_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa os e-mails em paralelo usando multiprocessing."""
        with Pool(processes=os.cpu_count()) as pool:
            results = []
            iterator = pool.imap(self._get_mail_content, mail_list)

            for result in tqdm(iterator, total=len(mail_list), desc="Downloading emails content"):
                if await request.is_disconnected():
                    print("Client disconnected, stopping processing...")
                    pool.terminate()
                    break
                if result:
                    results.append(result)

            pool.close()
            pool.join()
            return results


class DbFetcher:
    def __init__(self):
        pass

    async def get_csv_databses(
        self,
        request: Request,
    ):
        try:
           return {"data": sorted(os.listdir("./data/emails"), reverse=True)}
        except:
            return {"data": []}
            
        
        

    


















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