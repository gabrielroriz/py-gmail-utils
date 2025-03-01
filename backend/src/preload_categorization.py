from src.csv_handler import csv_to_dict
from src.google_apis import gmail_get_email_domain, GmailAPI

settings = csv_to_dict("./data/fr.csv")
mail_content = csv_to_dict("./data/emails.csv")

##########
# INIT #
##########
gmail_api = GmailAPI('client_secret.json')

##########
# LABELS #
##########
labels = gmail_api.list_labels()

domain_dict = {item["name"]: item for item in settings}

for mail in mail_content:
    mail_sender_domain = gmail_get_email_domain(mail["sender"])
    domain_settings = domain_dict.get(mail_sender_domain)

    # It has label?
    if domain_settings and domain_settings["label"] and len(domain_settings["label"]) > 0:
        print(domain_settings)

        # print(mail['sender'] + " - " + mail["label"])
    # else:
    # for setting in settings:
        # print(setting)



