from datetime import datetime 
import time
import pygame
import RPi.GPIO as GPIO
from button.button import Button
from sheets.saintquote import pick_quote
from sheets.g_calendar import Event
import sheets.g_calendar as gc
from alarm.alarm import Alarm
from subprocess import run

"""
File to hold the Susanna Class
"""


class Susanna:
    

    
    def __init__(self, monitor_power = True, button1 = Button(pin=8), button2 = Button(pin=10), 
                 button3=Button(pin=12), alarm = Alarm(), quote = pick_quote()):
        
        self.monitor_power = monitor_power
        self.button1 : Button = button1
        self.button2 : Button = button2
        self.button3 : Button = button3
        self.alarm : Alarm = alarm
        self.quote : str = quote

    def init_Susanna(self):

        # Initalize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # Initalize Alarms
        pygame.mixer.init()

        self.button1.init_button()
        self.button2.init_button()
        self.button3.init_button()

        self.alarm.init_alarm('Good_MorningV2.mp3')
        print("Susanna has been activated")


    def update_alarm(self, alarm):
        next_alarm = gc.get_next_alarm()
        if next_alarm == None:
            return
        else:
            alarm.hour = next_alarm.hour
            alarm.minute = next_alarm.minute
            alarm.day = next_alarm.day
            alarm.month = next_alarm.month


    def check_buttons_update(self):
        self.button1.button_switch()
        self.button2.button_switch()
        self.button3.button_switch()

    def toggle_monitor_power(self) -> bool:
        # if self.monitor_power:
        #     run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --off")
        #     self.monitor_power = not self.monitor_power
        #     return self.monitor_power
        # elif self.monitor_power:
        #     run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --on")
        #     self.monitor_power = not self.monitor_power
        #     return self.monitor_power
        return 0

        

        
