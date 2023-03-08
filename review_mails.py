import base64
import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = login()
    service = build('gmail', 'v1', credentials=creds)  
    result = service.users().messages().list(maxResults=500, userId='me', q="mailer-daemon@googlemail.com").execute()
    messages = result.get('messages') # messages is a list of dictionaries where each dictionary contains a message id.
    failures = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            email, delivery_incomplete, address_not_found = False, False, False
            headers = txt['payload']['headers']
            """if 'Your message to ' in txt['snippet']:
                email = txt['snippet'].split('Your message to ')[1].split(" coul")[0].replace(' ', '')
                if len(email) < 40:
                    failures.append(email)
            continue"""
            """if 'This is the mail system at host' in txt['snippet']:
                for part in txt['payload']['parts']:
                    if part['partId'] == '2':
                        for subpart in part['parts'][0]['headers']:
                            if subpart['name'] == 'To':
                                email = subpart['value']
                                print(email)
                failures.append(email)
            continue"""
            """for d in headers:
                if d['name'] == 'From' and d['value'] == 'asmecal':
                    print(txt['payload'])
                else:
                    continue
            email = str(base64.urlsafe_b64decode(txt['payload']['body']['data'])).split('<')[1].split('>')[0]
            for d in headers:
                if d['name'] == 'From' and d['value'] != 'mailer-daemon@googlemail.com': #Mail Delivery System <MAILER-DAEMON@csi.it>
                    for part in txt['payload']['parts']:
                        print(txt['payload']['parts'])
                        if part['partId'] == '2':
                            for subpart in part['parts'][0]['headers']:
                                if subpart['name'] == 'To':
                                    email = subpart['value']
                                    print(email)
                                    break"""
            for d in headers:
                if d['name'] == 'X-Failed-Recipients':
                    address_not_found = d['value']
            if not email:
                try:
                    delivery_incomplete = txt['snippet'].split("delivered to ")[1].split(' because t')[0]
                except:
                    pass
                email = address_not_found if address_not_found else delivery_incomplete
            failures.append(email)
        except HttpError as error:
            print(f'An error occurred: {error}')
    print(failures)

def login():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()