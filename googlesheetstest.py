import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/neast/Documents/Susan/secret_key.json", scopes=scope)

client = gspread.authorize(creds)
sheet = client.open('Susan_Saint_Quotes').sheet1
quote = sheet.cell(4,3).value
print(quote + ' - Saint Francis De Sales')

