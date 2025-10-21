from button.button import Button
from display.display import Display
import RPi.GPIO as GPIO
import time
from datetime import datetime
from subprocess import run
from enum import Enum
from logs.logs import log
from alarm.alarm import Alarm
from transistions import *
from lights.lights import LEDs

#Test Comment, this can be delelted
PIN1= 6
PIN2 = 5
ROTARY_PIN = 4

NUM_PIXELS = 59


class States(Enum):
    DEFAULT = 0
    SLEEP = 1
    WAKE = 2
    ALARM = 3


leds = LEDs(NUM_PIXELS, 0.4)
print(f"LEDs Initialized on pin {leds.pixel_pin}")
strip = leds.init_leds()
state = States.DEFAULT


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
button1 = Button(PIN1)
button2 = Button(PIN2)

button1.init_button()
button2.init_button()

log("Running")
log("Backend has started")


leds.startup(strip, (255, 255, 255))

while True:

    match state:
        # screen and leds on are on alarm is not playing
        case States.DEFAULT:
            if button1.press(): # display and leds turn off
                log("Button 1 pressed: Display is turning off: state is SLEEP")
                time.sleep(1)
                leds.off(strip)
                state = States.SLEEP


        # screen and leds are off       
        case States.SLEEP:
            if button1.press():
                log("Button 1 pressed: Display is turning On: state is DEFAULT")
                time.sleep(1)
                state = States.DEFAULT
                leds.display_color(strip, 255, 255, 255)
            
            

