from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime 
import time
import pygame
import RPi.GPIO as GPIO
from button.button import Button
from sheets.saintquote import pick_quote
import sheets.g_calendar as gc
from alarm.alarm import Alarm
from main import Susanna


"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilead'
socketio = SocketIO(app, cors_allowed_origins='*')

#app.register_blueprint(second, url_prefix="")


# class Susanna:
#     def __init__(self, button1, button2, button3, alarm, quote):
#         self.button1 : Button = button1
#         self.button2 : Button = button2
#         self.button3 : Button = button3
#         self.alarm : Alarm = alarm
#         self.quote : str = quote

# def init_Susanna():

#     # Initalize GPIO
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BOARD)

#     # Initalize Alarms
#     pygame.mixer.init()

#     suzy = Susanna(
#         button1 = Button(pin=8),
#         button2 = Button(pin=10),
#         button3 = Button(pin=12),
#         alarm = Alarm(hour=gc.get_event_hour(), minute=gc.get_event_hour(), day=gc.get_event_day(), month=gc.get_event_month()),
#         quote=pick_quote(),
#         )

#     suzy.button1.init_button()
#     suzy.button2.init_button()
#     suzy.button3.init_button()

#     suzy.alarm.init_alarm('Good_MorningV2.mp3')
#     print("Susanna has been activated")

#     return suzy

"""
Method to update the alarm if a new event is added in the calendar
"""
# def update_alarm(alarm):
#     alarm.hour = gc.get_event_hour
#     alarm.minute = gc.get_event_minute
#     alarm.day = gc.get_event_day
#     alarm.month = gc.get_event_month
#     return alarm


"""
In Background Thread loop whatever code you want to run continously. Then at the end have it emit the data you want
to send to the javascript.
"""
def background_thread():
    # Initalization Functions

    susanna = Susanna()
    susanna.init_Susanna()



    """
    Program that Continously Loops
    """
    while True:
        now = datetime.now()
        #susanna.alarm.play_alarm()
        susanna.check_buttons_update()
        susanna.toggle_monitor_power()

    #  Toggles Monitor Power
        monitor = susanna.button1.button_press()
        if monitor:
            #susanna.toggle_monitor_power()
            print(f"Monitor state is {susanna.monitor_power}")

        
        if now.second % 20 == 0 and now.microsecond > 100000:
            susanna.quote = pick_quote()
            #susanna.update_alarm(susanna.alarm)
            print(susanna.alarm.hour)

      

        if susanna.button2.state == True:
            susanna.alarm.stop = True
        else: 
            susanna.alarm.stop = False

        socketio.emit('updateData', {'quote': susanna.quote, 
                                    'Button1': susanna.button1.state, 
                                    'Button2': susanna.button2.state,
                                    'Button3': susanna.button3.state,
                                    'Calendar': susanna.alarm.hour})
        print(f"Button 1: {susanna.button1.state}\nButton 2: {susanna.button2.state}\nButton 3: {susanna.button3.state}")
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