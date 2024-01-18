import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import random


scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("secret_key.json", scopes=scope)

client = gspread.authorize(creds)
sheet = client.open('Susan_Saint_Quotes').sheet1

def pick_quote() -> str:
    saint = round(random() * (len(sheet.row_values(1)) - 1), 0)
    quote = round(random() * (len(sheet.col_values(saint+1)) - 2), 0)
    quote_picked = sheet.cell(quote+2, saint+1).value + ' - ' + sheet.cell(1, saint+1).value
    return quote_picked   