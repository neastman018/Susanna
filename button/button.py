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
    def __init__(self, pin = 0, state = False, pressed = False, last_press = time.time(), debounce : float  = 0.05):
        self.pin = pin
        self.state = state
        self.pressed = pressed
        self.last_press = last_press
        self.debounce = debounce
        self.button = None
        """
        Method to inialize the button
        @parameter pin is the pin number that the button is hooked up to
        """
    def init_button(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    """
    Method that will return a true false based on the state of the button press
    Button will act like a switch

    """ 
    def button_switch(self) -> bool:
        if GPIO.input(self.pin) == GPIO.HIGH and (time.time() - self.last_press) >= self.debounce and not self.pressed:
            self.pressed = True
            self.last_press = time.time()
            self.state = not self.state
            print(1)

        if GPIO.input(self.pin) == GPIO.LOW and self.pressed:
            self.pressed = False
            print(2)

        return self.state
    
    def button_press(self) -> bool:
        if GPIO.input(self.pin) == GPIO.HIGH and (time.time() - self.last_press) >= self.debounce and not self.pressed:
            self.pressed = True
            self.last_press = time.time()
            return self.pressed
        
        if GPIO.input(self.pin) == GPIO.LOW and self.pressed:
            self.pressed = False
            return self.pressed
    



