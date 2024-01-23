"""
Button Class
"""

import time
import RPi.GPIO as GPIO

class Button:
    """
    @parameter pin is the GPIO pin the button is hooked up to (pin number on board)
    @parameter state is whichever state variable the button is controlling
    @parameter last_press in the time of the last button press for debounce purposes
    """
    def __init__(self, pin = 0, state = False, last_press = time.time(), debounce : float  = 0.2):
        self.pin = pin
        self.state = state
        self.last_press = last_press
        self.debounce = debounce
        self.button = None
        """
        Method to inialize the button
        @parameter pin is the pin number that the button is hooked up to
        """
    def init_button(self, button_pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    """
    Method that will return a true false based on the state of the button press

    """ 
    def button_press(self) -> bool:
        if GPIO.input(self.pin) == GPIO.HIGH and (time.time() - self.last_press) >= self.debounce:
            self.last_press = time.time()
            self.state = not self.state

        return self.state
