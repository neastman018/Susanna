## 7/27/2025
# System Overview:
    Both Push buttons are functional, with hardware methods to interact. 
    However the right button has been observed as activily randomly, although this is infrequent

    Rotary Encoder including button is not functioning at all. Wiring has not been done

    Neo Pixels are working, however they are not running correctly on startup. 
    Think it is a problem with the RaspPi Trying to multitask -- cutting of Neo Pixel Sequence.

    Alarm is going off on time. However I know it will not working for mulitiple days consectrivily as the application only checks the time on start.

    Screen control is fucntioning correctly.

# TODO:
    1. Need to work to get lights functioning with buttons and wake up.
    2. Change the way the application checks for wake up time
    3. Implement a more interrupt based approach?