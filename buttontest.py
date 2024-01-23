import RPi.GPIO as GPIO
import time

buttonPin = 10

def button_callback(channel):
    print("button was pushed")



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=button_callback)

message = input("Press Button to quit \n \n")

GPIO.cleanup()
