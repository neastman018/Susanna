"""
Methods for setting and activating an alarm
"""
import multiprocessing
import pygame
from datetime import datetime 
import string

"""
Function to inteperate time 
"""
#def interperate_time(time):

"""
Method to initalize the alarm
@parameter alarm_sound: music file to play
"""

"""
Method to play the alarm
@parameter alarm: return of the init_alarm function which is a initalized alarm with a song loaded
@parameter alarm_time_hour: hour the alarm should go off (24 hour time)
@parameter alarm_time_minute: minute the alarm should go off
@parameter alarm_time_second: minute the alarm should go off (will be 00 by default)
@parameter stop: boolean value to stop the alarm
"""

class Alarm:

    def __init__(self, alarm = pygame.mixer.music, stop = False, active = False, hour = 0, minute = 0, second = 1, playing = False):
        self.alarm = alarm
        self.stop = stop
        self.active = active
        self.hour = hour
        self.minute = minute
        self.second = second
        self.playing = playing

        


    def init_alarm(self, alarm_sound):
        self.alarm.load("alarm/music/" + alarm_sound)
    
    def is_active(self) -> bool:
        return self.alarm.get_busy()
        

    def play_alarm(self) -> bool:
        now = datetime.now()
        #now.second does not register 0
        if self.second == 0:
            self.second = 1

        if self.hour == now.hour and self.minute == now.minute and self.second == now.second and not self.is_active():
            print(self.is_active())
            self.playing = True
            self.alarm.play()

        if self.stop and self.is_active():
            print("alarm is stopping")
            self.playing = False
            self.alarm.pause()

        return self.playing




          
           
    
