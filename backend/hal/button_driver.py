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
import time
import RPi.GPIO as GPIO

class ButtonDriver:
    def __init__(self, pin, debounce=0.05):
        self.pin = pin
        self.debounce = debounce
        self.pressed = False
        self.last_change_time = 0

        GPIO.setmode(GPIO.BCM)
        # Use a real GPIO pin like 17, 27, or 22. Avoid 0 or 1.
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def press(self) -> bool:
        current_state = GPIO.input(self.pin) == GPIO.HIGH
        now = time.time()

        # If the state has changed (physical movement)
        if current_state != self.pressed:
            # Check if enough time has passed to ignore "noise" (debounce)
            if (now - self.last_change_time) > self.debounce:
                self.pressed = current_state
                self.last_change_time = now
                if self.pressed:
                    print(f"Button on BCM {self.pin} Pressed")
                else:
                    print(f"Button on BCM {self.pin} Released")

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
    
  
        
