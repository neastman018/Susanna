"""
Button Class
"""
import time
import RPi.GPIO as GPIO
    
class ButtonDriver:
    """
    @parameter pin is the GPIO pin the button is hooked up to (pin number on board)
    @parameter state is whichever state variable the button is controlling
    @parameter last_press in the time of the last button press for debounce purposes
    """
    def __init__(self, pin = 0, state = False, pressed = False, triggered = False, last_triggered = time.time(), last_press = time.time(), debounce : float  = 0.1, hold : float = 0.01):
        self.pin = pin
        self.state = state
        self.pressed = pressed
        self.triggered = triggered # Will help filter out false positives
        self.last_triggered = last_triggered
        self.last_press = last_press
        self.debounce = debounce
        self.hold = hold
        self.button = None
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
        
    def press(self) -> bool:
        if time.time() - self.last_triggered > self.hold:
            self.triggered = False

        if GPIO.input(self.pin) == GPIO.HIGH and (time.time() - self.last_press) >= self.debounce and not self.pressed:
            if (time.time() - self.last_triggered) >= self.hold and not self.triggered:
                self.last_triggered = time.time()
                self.triggered = True
                print("Button Triggered")
            
            elif self.triggered:
                self.pressed = True
                self.last_press = time.time()
                self.triggered = False
                print("Button Pressed")

        elif GPIO.input(self.pin) == GPIO.LOW and (time.time() - self.last_press) >= self.debounce and self.pressed:
            self.pressed = False
            print("Button Released")

        return self.pressed

    """
    Method that will return a true false based on the state of the button press
    Button will act like a switch

    """ 
    def switch(self) -> bool:
        if GPIO.input(self.pin) == GPIO.HIGH and (time.time() - self.last_press) >= self.debounce and not self.pressed:
            self.pressed = True
            self.last_press = time.time()
            self.state = not self.state

        elif GPIO.input(self.pin) == GPIO.LOW and (time.time() - self.last_press) >= self.debounce and self.pressed:
            self.pressed = False

        return self.state
    
    def cleanup(self):
        GPIO.cleanup(self.pin)
    
  
        
