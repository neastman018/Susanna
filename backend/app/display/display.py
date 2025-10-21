
from subprocess import run
from time import sleep

class Display:

    def __init__(self, state = True):
        self.state = state
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --transform 270", shell=True)


    def turn_on_display(self):
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --on", shell=True)
        sleep(1) # sleep for 1 second or the display will disconnect
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --transform 270", shell=True)
        self.state = True


        sleep(1) # Give the display a change to turn on before you do anything
        return True

    def turn_off_display(self):
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --off", shell=True)
        self.state = False
        sleep(1) # Give the display a change to turn on before you do anything
        return False
    

if __name__ == "__main__":
    display1 = Display()
    display1.turn_off_display()
