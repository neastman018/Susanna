from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from dataclasses import dataclass
from datetime import datetime 
import time
import RPi.GPIO as GPIO
import RPi.GPIO as GPIO 
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


@dataclass
class Susanna:
    b1_debounce: int
    stop: bool
    alarm_active: bool
    quote: str

    def __init__(self, b1_debounce, stop, alarm_active, quote, b1pin):
        self.b1_debounce = b1_debounce
        self.stop = stop
        self.alarm_active = alarm_active
        self.quote = quote
        self.b1pin = b1pin

def init_Susanna():
    suzy = Susanna(
        b1_debounce = time.time(), 
        stop = False, 
        alarm_active = True, 
        quote=pick_quote(),
        b1pin = 10
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
    global stop
    stop = False
    buttonPin = 10

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  



    while True:
        now = datetime.now()
        susanna.b1_debounce = time.time()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(susanna.b1pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if now.second % 20 == 0 and now.microsecond > 200000:
            susanna.quote = pick_quote()
            #print(quote_picked)


        play_alarm(alarm, susanna.stop, 16, 9, 0)

        if now.second == 30:
            susanna.stop = True
            
        play_alarm(alarm, 9, 15, 0)
        stop_alarm(alarm, stop)


        #print(stop)
        socketio.emit('updateData', {'quote': susanna.quote, 'processor_time': susanna.b1_debounce})
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
