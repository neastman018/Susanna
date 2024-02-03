import gspread
from oauth2client.service_account import ServiceAccountCredentials
from random import random
from datetime import datetime


scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/neast/Susanna/susanna/sheets/skey.json', scopes=scope)

client = gspread.authorize(creds)
sheet = client.open('Susan_Saint_Quotes').sheet1

def pick_quote() -> str:
    saint = round(random() * (len(sheet.row_values(1)) - 1), 0)
    quote = round(random() * (len(sheet.col_values(saint+1)) - 2), 0)
    quote_picked = sheet.cell(quote+2, saint+1).value + ' - ' + sheet.cell(1, saint+1).value
    return quote_picked   


"""
Overall Method to shuffle the quote being diplayed
@parameter interval: roughly the inveral in seconds that the quote is shuffled (1-60)
@paramter sleep_time is the time the thread sleeps between interations
"""
def shuffle_quotes(interval, sleep_time, now) -> str:
    sleep_time = sleep_time * 1000000
    if now.second % interval == 0 and now.microsecond <= sleep_time:
        quote_picked = pick_quote()
        #print(quote_picked)
        return quote_picked
    

    if __name__ == "__main__":
        print(pick_quote())
       
    

    