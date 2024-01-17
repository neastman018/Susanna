from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime 
from random import random
from alarm.alarm import play_alarm
import gspread
from oauth2client.service_account import ServiceAccountCredentials

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilead'
socketio = SocketIO(app, cors_allowed_origins='*')

#app.register_blueprint(second, url_prefix="")

#Google Sheets Validation Nonsense
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/neast/Documents/Susan/secret_key.json", scopes=scope)

client = gspread.authorize(creds)
sheet = client.open('Susan_Saint_Quotes').sheet1

def pickquote():
        saint = round(random() * 2, 0)
        quote = round(random() * 4, 0)
        quote_picked = sheet.cell(quote+2, saint+1).value + ' - ' + sheet.cell(1, saint+1).value
        return quote_picked


"""
In Background Thread loop whatever code you want to run continously. Then at the end have it emit the data you want
to send to the javascript.
"""
def background_thread():
    alarm_active = False
    quote_picked = pickquote()
    while True:
        now = datetime.now()
        quote_picked = pickquote()

        play_alarm(19, 36, alarm_sound='Good_MorningV2.mp3')

        socketio.emit('updateData', {'quote': quote_picked})
        socketio.sleep(1)
    
    



@app.route('/')

def index():
    return render_template("index.html")


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=80)