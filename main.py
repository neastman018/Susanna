from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime 
from random import random
from alarm.alarm import play_alarm
"""    
This is the file that will contain the initialization methods and the run mentod
"""    
def init():
    alarm_active = False

def run_Susan(socketio):
    now = datetime.now()
    dummy_sensor_value = round(random() * 100, 3)
    play_alarm(13, 48, alarm_sound='Good_MorningV2.mp3')
    socketio.emit('updateData', {'value': dummy_sensor_value, "date": now.strftime("%m/%d/%Y %H:%M:%S")})
    socketio.sleep(1)

def run():
    init()
    while True:
        run_Susan()

