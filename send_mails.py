import base64
import os.path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token_send.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#credentials sheets
client_secret_file = 'credentials_sheets.json'
googleScope = ['https://www.googleapis.com/auth/spreadsheets']
googleCredentials = service_account.Credentials.from_service_account_file(client_secret_file, scopes=googleScope)
spreadsheet_id = '1mrp9rbA1N4QAVLXElPQf-pUmh9Tjy59O1lmuBdJdbGc'
service = build('sheets', 'v4', credentials=googleCredentials)
spreadsheet = service.spreadsheets().values()

def main():
    creds = login()
    service = build('gmail', 'v1', credentials=creds)
    send_snd(service)

def send_snd(service):
    sheet = spreadsheet.get(spreadsheetId=spreadsheet_id, range='List').execute().get('values')
    sheet.pop(0)
    for comune in sheet:
        if (comune[6] == 'FALSE' or comune[7] == 'FALSE') and comune[8] != 'todo':
            try:
                message = create_message(comune[8], body.replace('(Comune)', comune[0]))
                send_message(service, message)
            except HttpError as error:
                print(comune[0])
                print(f'An error occurred: {error}')

def send_fst(service):
    sheet = spreadsheet.get(spreadsheetId=spreadsheet_id, range='List').execute().get('values')
    sheet.pop(0)
    for comune in sheet:
        if comune[5] != '' and comune[6] == 'FALSE':
            try:
                message = create_message(comune[5], body.replace('(Comune)', comune[0]))
                send_message(service, message)
            except HttpError as error:
                print(f'An error occurred: {error}')
                print(comune[0])

body = """
<html>
    <body>
        <font size="4">
            <br>Comune di (Comune)<br><br>

            <b>Gentile Signore/a:</b><br>

            &ensp;Buongiorno, Il mio nome è Agustín Ferré e sto pensando di andare a vivere in Italia e risiedere nel comune per richiedere la mia cittadinanza italiana.<br>
            
            Mi rivolgo a Lei al fine di consultarla riguardo ai requisiti per fare il riconoscimento della mia cittadinanza italiana 
            Iure sanguinis in questo comune giacché ogni comune implementa le sue varianti.<br><br>
            
            Vorrei anche consultare:<br>

        </font>
        <ul style="margin:0; margin-left: 25px; padding:0; font-family: Arial; font-size:18px; line-height:35px;" align="left" type="disc">
            <li>
                I documenti hanno una <b>scadenza determinata</b> dalla loro data di rilascio?<br>
            </li>

            <li>
                È necessario presentare <b>certificati di morte</b>? o solo quelli di nascita e matrimonio?<br>
            </li>

            <li>
                È necessario prendere un <b>appuntamento</b> per fare la residenza? e per presentare la mia cartella di cittadinanza?<br>
            </li>

            <li>
                Negli atti argentini, il mio AVO presenta una variazione del suo nome e cognome, sul suo certificato di nascita 
                italiano appare come <i>Leone Carmine Montisarchio</i>, 
                ma nel resto dei certificati argentini appare come <i>León Montesarchio</i>. 
                Non è possibile rettificarlo nello stato civile perché ciò implicherebbe un cambiamento di identità per tutte le 
                persone della linea di discendenza. Vorrei sapere se questo tipo di variazione è accettata in quanto è <b>esplicitamente 
                verificabile attraverso il resto degli atti</b> che si tratti della stessa persona e <b>la variante è nel certificato di non 
                naturalizzazione argentino</b>.<br><br>
            </li>

        </ul>
        <font size="4">

            Grazie per la collaborazione, colgo l’occasione per salutarvi con la mia massima considerazione.<br><br>

            Agustín Ferré
        </font>
    </body>
</html>
"""

def create_message(to, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['From'] = 'Agustín Ferré'
    message['subject'] = 'Consultazione Cittadinanza'
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }

def send_message(service, message):
  try:
    message = service.users().messages().send(userId='agusferrex@gmail.com', body=message).execute()
  except Exception as e:
    print('An error occurred: %s' % e)
    return None

def login():
    creds = None
    if os.path.exists('token_send.json'):
        creds = Credentials.from_authorized_user_file('token_send.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_send.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()