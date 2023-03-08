from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time

#credentials sheets
client_secret_file = 'credentials_sheets.json'
googleScope = ['https://www.googleapis.com/auth/spreadsheets']
googleCredentials = service_account.Credentials.from_service_account_file(client_secret_file, scopes=googleScope)
spreadsheet_id = '1mrp9rbA1N4QAVLXElPQf-pUmh9Tjy59O1lmuBdJdbGc'
service = build('sheets', 'v4', credentials=googleCredentials)
spreadsheet = service.spreadsheets().values()

def sheet_scraper(driver):
    sheet = spreadsheet.get(spreadsheetId=spreadsheet_id, range='List').execute().get('values')
    sheet.pop(0)
    body = {
        'value_input_option': 'RAW',
        'data': {}
    }
    for i, comune in enumerate(sheet):
        if comune[6] == 'FALSE' or comune[7] == 'FALSE':
            if len(comune) < 9 or comune[8] == '' or comune[8] == 'first':
                print(comune[0])
                try:
                    time = 'first' if len(comune) < 9 or comune[8] == '' else 'todo'
                    body['data'] = {"range": 'List!I' + str(i + 2), "values": [[time]]}
                    spreadsheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
                    driver.get('http://' + comune[4])
                    if time != 'first':
                        mail = driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]').get_attribute('href').split('mailto:')[1]
                        body['data'] = {"range": 'List!I' + str(i + 2), "values": [[mail]]}
                    else:
                        elem = driver.find_element(By.CSS_SELECTOR, 'a.cryptedmail')
                        mail = elem.get_attribute('data-name') + '@' + elem.get_attribute('data-domain') + '.it'
                        body['data'] = {"range": 'List!I' + str(i + 2), "values": [[mail]]}
                    print(mail)
                    spreadsheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
                except HttpError as error:
                        print(f'An error occurred: {error}')
                        print(comune[0])
    driver.close()

def comuni_scraper(driver):
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    for i in range(1, 111):
        i = '0' + str(i) if i < 10 else str(i)
        i = '0' + i if int(i) < 100 else i
        time.sleep(2)
        driver.get('http://www.comuni-italiani.it/' + i + '/index.html')
        time.sleep(3)
        province = driver.find_element(By.TAG_NAME, 'h1').text.split("Provincia di ")[1]
        region = driver.find_element(By.CSS_SELECTOR, '.ival a').text
        comuni = len(driver.find_elements(By.CSS_SELECTOR, '.tabwrap [width="33%"] a'))
        comuni_arr = []
        for j in range(0, comuni):
            time.sleep(1.3)
            comune = driver.find_elements(By.CSS_SELECTOR, '.tabwrap [width="33%"] a')[j]
            comune_arr = [comune.text, province, region]
            comune.click()
            time.sleep(1.3)
            try:
                pop = driver.find_element(By.CSS_SELECTOR, 'td [align="center"] b').text.replace('.', '')
                comune_arr.append(pop)
                site = driver.find_element(By.XPATH, "//*[text()='Sito Ufficiale']").get_attribute('href').split('://')[1]
                comune_arr.append(site)
                mail = driver.find_element(By.XPATH, "//*[text()='Email Comune']").get_attribute('href').split('mailto:')[1]
                comune_arr.append(mail)
            except:
                comune_arr.append('')
            #storeToSheet(comune_arr)
            print(comune_arr)
            comuni_arr.append(comune_arr)
            driver.back()
    driver.close()

def storeToSheet(row):
    body = {
        'range': 'test',
        'values': [row],
        'majorDimension': 'ROWS'
    }
    spreadsheet.append(spreadsheetId=spreadsheet_id, range='test', valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()

if __name__ == '__main__':
    main()