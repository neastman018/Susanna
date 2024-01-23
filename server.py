from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from dataclasses import dataclass
from datetime import datetime 
import time
import RPi.GPIO as GPIO
from button.button import Button
from sheets.saintquote import pick_quote
from alarm.alarm import play_alarm, init_alarm


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
    def __init__(self, button, stop, alarm_active, quote):
        self.button : Button = button
        self.stop : bool = stop
        self.alarm_active : bool = alarm_active
        self.quote : str = quote

def init_Susanna():
    suzy = Susanna(
        button = Button(),
        stop = False, 
        alarm_active = True, 
        quote=pick_quote(),
        )
    
    print("Susanna has been activated")

    return suzy



"""
In Background Thread loop whatever code you want to run continously. Then at the end have it emit the data you want
to send to the javascript.
"""
def background_thread():
    # Initalization Functions
    susanna = init_Susanna()
    alarm = init_alarm('Good_MorningV2.mp3')

    """
    Program that Continously Loops
    """
    while True:
        now = datetime.now()
        susanna.stop = susanna.button.button_press()
        print(susanna.stop)
        if now.second % 20 == 0 and now.microsecond > 200000:
            susanna.quote = pick_quote()
            #print(quote_picked)

        play_alarm(alarm, susanna.stop, 16, 9, 0)

        if now.second == 30:
            susanna.stop = True
        else: 
            susanna.stop = False

        #print(stop)
        socketio.emit('updateData', {'quote': susanna.quote, 'processor_time': susanna.button.state})
        socketio.sleep(.2)
    
    


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