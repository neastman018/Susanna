from button.button import Button
from display.display import Display
import RPi.GPIO as GPIO
import time
from datetime import datetime
from subprocess import run
from enum import Enum
from alarm.alarm import Alarm
from transistions import *
import os
from lights.lights import LEDs
import json

# Define Button Pins
PIN1= 6
PIN2 = 5
ROTARY_PIN = 4

# Define the Different States
class States(Enum):
    DEFAULT = 0
    SLEEP = 1
    WAKE = 2
    ALARM = 3

NUM_PIXELS = 60
DEFAULT_COLOR = (255, 255, 255)


# Initalize the Display
display = Display()

# Define the Inital State
state = 0


# Initalize the Alarms
morning_alarm = Alarm()

with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            alarm_sound = config.get('ALARM', {}).get('ALARM_SOUND', [])
            print(f"Wake up time for today: {alarm_sound}")
morning_alarm.init(alarm_sound)

alarm2 = Alarm()
alarm2.init("Peaky_Blinders.mp3")
study_music = Alarm()
study_music.init("study_chants.mp3")
sleep_sounds = Alarm()
sleep_sounds.init("rain_noise.mp3")


# Initalize the Buttons
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
button1 = Button(PIN1)
button2 = Button(PIN2)
encoder_button = Button(ROTARY_PIN)

button1.init_button()
button2.init_button()
encoder_button.init_button()

print("Running")
print("Backend has started")

# Check if the script is running as sudo
SUDO = False
leds = LEDs(NUM_PIXELS, 0.4)
strip = leds.init_leds()


if os.geteuid() == 0: # Root User Returns 0
    SUDO = True
    print("Running as SUDO")
    time.sleep(10)  # Wait for the system to stabilize
    leds.startup(strip, DEFAULT_COLOR)
    leds.startup(strip, (255, 255, 255))

else:
    SUDO = False

while True:
    playing_alarm = alarm2 # keeps track of what alarm is being played, so we can manipulate the active one.
    morning_alarm.wake_up()
    match state:
        # screen and leds on are on alarm is not playing
        case 0:
            if button1.press(): # display and leds turn off
                print(f"Button 1 pressed: Display is turning off: state is SLEEP ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                if SUDO:
                    leds.off(strip)
                else:
                    display.turn_off_display()

                state = 1
                time.sleep(0.5)



            if button2.press(): # play music
                print(f"Button 2 Pressed: Music Turning On ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                if SUDO:
                    leds.display_color(strip, 255, 255, 255)
                else:
                    study_music.play_alarm()
                    playing_alarm = study_music

                time.sleep(0.5)
                state = 3


            if encoder_button.press():
                print(f"Encoder Button Pressed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = default_encoder_button(study_music)
                playing_alarm = study_music

            elif morning_alarm.is_active():
                print(f"Alarm is Active ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = default_alarm()

        # screen and leds are off       
        case 1:
            if button1.press():
                print(f"Button 1 pressed: Display is turning On: state is DEFAULT ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                if SUDO:
                    leds.display_color(strip, 255, 255, 255)
                else:
                    display.turn_on_display()

                time.sleep(0.5)
                state = 0

            if button2.press():
                print("Button 2 Pressed: Music Turning On")
                state = sleep_button2(sleep_sounds)
                playing_alarm = sleep_sounds

            if encoder_button.press():
                print(f"Encoder Button Pressed ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = sleep_encoder_button(sleep_sounds)
                playing_alarm = sleep_sounds
            
            elif morning_alarm.is_active():
                print(f"Alarm is Active ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = sleep_alarm(display)
            
            
        case 2:
            if SUDO:
                leds.display_color(strip, 255, 255, 255)
            
            if button1.press() or button2.press():
                print(f"Button 1 or 2 pressed: Alarm is turning off: state is DEFAULT ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                if SUDO:
                    # Do Nothing for now
                    continue
                else:
                    playing_alarm.alarm_stop()

                time.sleep(0.5)
                state = 0
                
            elif not playing_alarm.is_active():
                print(f"Alarm Finished ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = alarm_alarm_end(playing_alarm)

        # Alarm is playing    
        case 3:
            if button1.press():
                print(f"Button 1 pressed: Display is turning off: state is still ALARM ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = alarm_button1(display)
            if button2.press():
                print(f"Button 2 Pressed: Music Turning Off ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                if SUDO:
                    leds.display_color(strip, 255, 255, 255)
                else:
                    playing_alarm.alarm_stop()
                
                time.sleep(0.5)
                state = 0
                
            elif not playing_alarm.is_active():
                print(f"Alarm Finished ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                state = alarm_alarm_end(playing_alarm)


