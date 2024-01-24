from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from dataclasses import dataclass
from datetime import datetime 
import time
import pygame
import RPi.GPIO as GPIO
from button.button import Button
from sheets.saintquote import pick_quote
from alarm.alarm import Alarm


"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilead'
socketio = SocketIO(app, cors_allowed_origins='*')

#app.register_blueprint(second, url_prefix="")


class Susanna:
    def __init__(self, button, alarm, quote):
        self.button : Button = button
        self.alarm : Alarm = alarm
        self.quote : str = quote

def init_Susanna():

    # Initalize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Initalize Alarms
    pygame.mixer.init()

    suzy = Susanna(
        button = Button(pin=10),
        alarm = Alarm(hour=13, minute=11, second=0),
        quote=pick_quote(),
        )

    suzy.button.init_button()
    suzy.alarm.init_alarm('Good_MorningV2.mp3')
    print("Susanna has been activated")

    return suzy



"""
In Background Thread loop whatever code you want to run continously. Then at the end have it emit the data you want
to send to the javascript.
"""
def background_thread():
    # Initalization Functions

    susanna = init_Susanna()


    """
    Program that Continously Loops
    """
    while True:
        now = datetime.now()
        susanna.alarm.play_alarm()
        susanna.button.button_press()
        
        if now.second % 20 == 0 and now.microsecond > 100000:
            susanna.quote = pick_quote()
            #print(quote_picked)

        

        if now.second == 30:
            susanna.alarm.stop = True
        else: 
            susanna.alarm.stop = False

        #print(stop)
        socketio.emit('updateData', {'quote': susanna.quote, 'processor_time': susanna.button.state})
        socketio.sleep(.1)
    
    


"""
===============================================================================================================================
Runs the site and renders the screen, all code goes above this portion
================================================================================================================================
"""
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
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)