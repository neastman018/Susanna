from subprocess import run
from app.services.application_state_service import ASService
from time import sleep

class ScreenService:
    def __init__(self, app_state: ASService):
        self.app_state = app_state
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --transform 270", shell=True)


    def turn_on_display(self):
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --on", shell=True)
        sleep(1) # sleep for 1 second or the display will disconnect
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --transform 270", shell=True)
        self.app_state.set_screen_state(True)
        sleep(1) # Give the display a change to turn on before you do anything
        return True

    def turn_off_display(self):
        run("WAYLAND_DISPLAY='wayland-1' wlr-randr --output HDMI-A-1 --off", shell=True)
        self.app_state.set_screen_state(False)
        sleep(1) # Give the display a change to turn on before you do anything
        return False
    
    def toggle_display(self):
        if self.app_state.get_screen_state():
            return self.turn_off_display()
        else:
            return self.turn_on_display()
    


