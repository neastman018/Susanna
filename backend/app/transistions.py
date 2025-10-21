"""
File to hold all the different state transitions
"""
from button.button import Button
from display.display import Display
import RPi.GPIO as GPIO
import time
from datetime import datetime
from subprocess import run
from enum import Enum
from logs.logs import log
from alarm.alarm import Alarm
from lights.lights import LEDs


#================================================================================================
#================================================================================================

def default_button1(display) -> int:

    display.turn_off_display()
    time.sleep(0.5)
    return 1

def default_button2(alarm) -> int:
    alarm.play_alarm()
    time.sleep(0.5)
    return 3

def default_encoder_button(alarm) -> int:
    alarm.play_alarm()
    time.sleep(0.5)
    return 3

def default_alarm() -> int:
    time.sleep(0.5)
    return 2

#================================================================================================
#================================================================================================

def sleep_button1(display) -> int:
    display.turn_on_display()
    time.sleep(0.5)
    return 0

def sleep_button2(alarm) -> int:
    alarm.play_alarm()
    time.sleep(0.5)
    return 3

def sleep_encoder_button(alarm) -> int:
    alarm.play_alarm()
    time.sleep(0.5)
    return 3

def sleep_alarm(display) -> int:
    display.turn_on_display()
    time.sleep(0.5)
    return 2

#================================================================================================
#================================================================================================

def alarm_button1(display) -> int:
    display.turn_off_display()
    return 3

def alarm_button2(alarm) -> int:
    alarm.alarm_stop()
    time.sleep(0.5)
    return 0

def alarm_alarm_end(alarm) -> int:  
    alarm.play_alarm(alarm)
    time.sleep(0.5)
    return 3

#================================================================================================
#================================================================================================



