import os
import base64

import re

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class GmailAPI:
    service = None
    
    def __init__(self, client_file, api_name='gmail', api_version='v1', scopes=['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.modify']):
        if self.service is None:
            self.service = self._create_service(client_file, api_name, api_version, scopes)
        else:
            pass

    def _create_service(self, client_secret_file, api_name, api_version, scopes, token_file='token.json'):
        """
        Creates a service with persistent OAuth credentials.

        Args:
            client_secret_file: Path to the client secret JSON file.
            api_name: Name of the API (e.g., 'gmail').
            api_version: Version of the API (e.g., 'v1').
            scopes: List of scopes for the API.
            token_file: Path to the token file for storing credentials.

        Returns:
            A service object for interacting with the API.
        """
        creds = None

        # Check if token file exists
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, scopes)

        # If no valid credentials, perform OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials to the token file
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        # Build and return the service
        try:
            service = build(api_name, api_version, credentials=creds)
            # print(f"{api_name} {api_version} service created successfully.")
            return service
        except Exception as e:
            print(f"Failed to create service instance: {e}")
            return None

    def _extract_body(self, payload):
        body = '<Text body not available>'
        
        if 'parts' in payload:
            for part in payload['parts']:
                # Caso o mimeType seja multipart/alternative, processa as subpartes
                if part['mimeType'] == 'multipart/alternative' and 'parts' in part:
                    for subpart in part['parts']:
                        if subpart['mimeType'] == 'text/plain' and 'body' in subpart and 'data' in subpart['body']:
                            body = base64.urlsafe_b64decode(subpart['body']['data']).decode('utf-8')
                            return body  # Retorna o texto assim que encontrado
                    
                # Caso contrário, verifica diretamente no nível atual
                if 'body' in part and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    return body
        
        # Verifica o corpo no nível raiz do payload (fallback)
        if 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body

    def get_mail_list(self, user_id='me', label_ids=None, folder_name='INBOX', max_results=5): 
        messages = []
        next_page_token = None

        if folder_name:
            label_results = self.service.users().labels().list(userId=user_id).execute()
            labels = label_results.get('labels', [])
            folder_label_id = next((label ['id'] for label in labels if label['name'].lower() == folder_name.lower()), None)
            if folder_label_id:
                if label_ids:
                    label_ids.append(folder_label_id)
                else:
                    label_ids = [folder_label_id]
            else:
                raise ValueError(f"Folder '{folder_name}' not found.")

        while True:
            result = self.service.users().messages().list(
                userId=user_id,
                labelIds=label_ids,
                maxResults=min(500, max_results - len(messages)) if max_results else 500,
                pageToken=next_page_token
            ).execute()
            
            messages.extend(result.get('messages', []))
            next_page_token = result.get('nextPageToken')
            if not next_page_token or (max_results and len(messages) >= max_results):
                break

        return messages[:max_results] if max_results else messages

    def get_mail_content(self, msg_id):
        message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = message['payload']
        headers = payload.get('headers', [])

        # Extrair informações básicas
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), None) or 'No subject'
        sender = next((header['value'] for header in headers if header['name'] == 'From'), 'No sender')
        recipients = next((header['value'] for header in headers if header['name'] == 'To'), 'No recipients')
        snippet = message.get('snippet', 'No snippet')
        has_attachments = any(part.get('filename') for part in payload.get('parts', []) if part.get('filename'))
        date = next((header['value'] for header in headers if header['name'] == 'Date'), 'No date')
        star = 'STARRED' in message.get('labelIds', [])
        label = ', '.join(message.get('labelIds', []))

        # Verificar se há link de unsubscribe
        unsubscribe_link = next((header['value'] for header in headers if header['name'].lower() == 'list-unsubscribe'), None)
        has_unsubscribe = unsubscribe_link is not None

        body = self._extract_body(payload)

        return {
            'id': msg_id,
            'subject': subject,
            'sender': sender,
            'recipients': recipients,
            'body': body,
            'snippet': snippet,
            'has_attachments': has_attachments,
            'date': date,
            'star': star,
            'label': label,
            'has_unsubscribe': has_unsubscribe,
            'unsubscribe_link': unsubscribe_link  # Opcional: retorna o link
        }

    def add_label_to_email(self, msg_id, label_id, user_id='me'):
        """
        Adiciona um marcador a um e-mail específico.

        Args:
            service: Serviço da API do Gmail criado com create_service.
            user_id: ID do usuário (geralmente 'me' para o usuário autenticado).
            msg_id: ID da mensagem (e-mail) a ser marcada.
            label_id: ID do marcador a ser adicionado.

        Returns:
            Response da operação de modificação do e-mail.
        """
        try:
            # Define a solicitação para modificar marcadores
            request_body = {
                'addLabelIds': [label_id],
                'removeLabelIds': []
            }

            # Executa a modificação na mensagem
            response = self.service.users().messages().modify(
                userId=user_id,
                id=msg_id,
                body=request_body
            ).execute()
            return response
        except Exception as e:
            print(f"Erro ao adicionar marcador ao e-mail: {e}")
            return None

    def list_labels(self, user_id='me'):
        """
        Lista todos os marcadores disponíveis na conta do usuário.

        Args:
            service: Serviço da API do Gmail criado com create_service.
            user_id: ID do usuário (geralmente 'me' para o usuário autenticado).

        Returns:
            Uma lista de dicionários contendo os IDs e nomes dos marcadores.
        """
        try:
            # Recupera a lista de marcadores
            labels = self.service.users().labels().list(userId=user_id).execute()
            labels_list = labels.get('labels', [])

            if not labels_list:
                print("Nenhum marcador encontrado.")
                return []

            # for label in labels_list:
            #    print(f"ID: {label['id']} | Nome: {label['name']}")

            return labels_list
        except Exception as e:
            print(f"Erro ao listar marcadores: {e}")
            return []

    def archive_email(self, msg_id, user_id='me'):
        """
        Arquiva um e-mail específico removendo o marcador INBOX.

        Args:
            service: Serviço da API do Gmail criado com create_service.
            user_id: ID do usuário (geralmente 'me' para o usuário autenticado).
            msg_id: ID da mensagem (e-mail) a ser arquivada.

        Returns:
            Response da operação de arquivamento do e-mail.
        """
        try:
            # Define a solicitação para remover o marcador INBOX
            request_body = {
                'addLabelIds': [],
                'removeLabelIds': ['INBOX']
            }

            # Executa a modificação na mensagem
            response = self.service.users().messages().modify(
                userId=user_id,
                id=msg_id,
                body=request_body
            ).execute()

            print(f"E-mail com ID: {msg_id} arquivado com sucesso.")
            return response
        except Exception as e:
            print(f"Erro ao arquivar o e-mail: {e}")
            return None

    def create_label(self, label_name, user_id='me'):
        """
        Cria um novo marcador na conta do Gmail.

        Args:
            service: Serviço da API do Gmail criado com create_service.
            label_name: Nome do marcador a ser criado.
            user_id: ID do usuário (geralmente 'me' para o usuário autenticado).

        Returns:
            O objeto do marcador criado ou None em caso de erro.
        """
        try:
            # Define o corpo da solicitação para criar o marcador
            label_body = {
                "name": label_name,
                "labelListVisibility": "labelShow",  # Mostra o marcador na interface do Gmail
                "messageListVisibility": "show"     # Mostra mensagens com esse marcador na lista
            }

            # Cria o marcador
            response = self.service.users().labels().create(
                userId=user_id,
                body=label_body
            ).execute()
            
            return response
        except Exception as e:
            print(f"Erro ao criar marcador '{label_name}': {e}")
            return None
        
    def create_filter(self, sender_email):
        label_name = f"{sender_email}"
        label_id = None

        labels = self.list_labels(user_id="me")

        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
                break
        
        if not label_id:
            new_label = self.create_label(label_name, user_id="me")
            label_id = new_label['id'] if new_label else None
            
        if not label_id:
            print(f"Não foi possível criar ou encontrar o marcador '{label_name}'.")
            return

        try:
            # Define o critério do filtro
            filter_object = {
                'criteria': {
                    'from': sender_email  # Mail
                },
                'action': {
                    'addLabelIds': [label_id], # Add Label
                    'removeLabelIds': ['INBOX']  # Archive
                }
            }
            # Cria o filtro
            result = self.service.users().settings().filters().create(userId='me', body=filter_object).execute()
            print('Filtro criado:', result)

            # Realiza a busca pelas mensagens que correspondem ao filtro
            query = f'from:{sender_email.strip()} is:inbox'
            results = self.service.users().messages().list(userId='me', q=query, maxResults=2000).execute()
            messages = results.get('messages', [])

            if not messages:
                print('Nenhuma mensagem encontrada.')
            else:
                for message in messages:
                    msg = self.service.users().messages().get(userId='me', id=message['id']).execute()

                    # Aplica as ações (arquivar e adicionar etiqueta)
                    self.service.users().messages().modify(
                        userId='me',
                        id=message['id'],
                        body={
                            'addLabelIds': [label_id],   # Adiciona a etiqueta
                            'removeLabelIds': ['INBOX']  # Remove da Caixa de Entrada (arquiva)
                        }
                    ).execute()

                print(f'{len(messages)} mensagens modificadas.')
            return result

        except Exception as error:
            print(f'Ocorreu um erro ao criar o filtro: {error}')
            return None
    

def gmail_get_email_domain(text):
    """
    Extrai o domínio (parte após o @, incluindo o @) de um e-mail presente na string.
    
    :param text: String que contém o e-mail dentro de "<>".
    :return: O domínio do e-mail (incluindo o @) ou None se não for encontrado.
    """
    if not text:
        return None

    email_regex = r"<([^>]+)>"
    match = re.search(email_regex, text, re.IGNORECASE)  
    
    if match:
        email = match.group(1)  # Extrai o e-mail completo
        at_domain = email[email.index('@'):]  # Pega o @ e o que vem depois
        return at_domain
    return None

def gmail_get_email(text):
    """
    Extrai o e-mail de uma string no formato "Texto <email@example.com>".
    
    :param text: String que contém o e-mail dentro de "<>".
    :return: O e-mail extraído ou None se não for encontrado.
    """
    email_regex = r"<([^>]+)>"
    match = re.search(email_regex, text, re.IGNORECASE)
    return match.group(1) if match else None

def gmail_get_label_by_name(labels, name):
    for label in labels:
        if label['name'] == name:
            return label
            
    return None








