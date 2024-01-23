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
def init_alarm(alarm_sound):
    pygame.mixer.init()
    alarm = pygame.mixer.music
    alarm.load("alarm/music/" + alarm_sound)
    return alarm

"""
Method to play the alarm
@parameter alarm: return of the init_alarm function which is a initalized alarm with a song loaded
@parameter alarm_time_hour: hour the alarm should go off (24 hour time)
@parameter alarm_time_minute: minute the alarm should go off
@parameter alarm_time_second: minute the alarm should go off (will be 00 by default)
@parameter stop: boolean value to stop the alarm
"""
def play_alarm(alarm, stop, alarm_time_hour, alarm_time_minute, alarm_time_second = 1):
    now = datetime.now()
    #now.second does not register 0
    if alarm_time_second == 0:
        alarm_time_second = 1

    if alarm_time_hour == now.hour and alarm_time_minute == now.minute and alarm_time_second == now.second and not alarm.get_busy():
        print(alarm.get_busy())
        alarm.play()

    if stop is True:
        print("alarm is stopping")
        alarm.pause()




          
           
    
