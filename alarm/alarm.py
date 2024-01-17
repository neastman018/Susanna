"""
Methods for setting and activating an alarm
"""
import multiprocessing
from playsound import playsound
from datetime import datetime 
import string

"""
Function to inteperate time 
"""
#def interperate_time(time):

"""
Method to play the alarm
@parameter alarm_time_hour: hour the alarm should go off (24 hour time)
@parameter alarm_time_minute: minute the alarm should go off
@parameter alarm_time_second: minute the alarm should go off (will be 00 by default)
@parameter alarm_sound: sound file to play when the alarm goes off
"""
def play_alarm(alarm_time_hour, alarm_time_minute, alarm_time_second = 0, alarm_sound = "example.wav"):
    now = datetime.now()
    alarm = multiprocessing.Process(target=playsound, args=("alarm/music/" + alarm_sound,))

    if alarm_time_hour == now.hour and alarm_time_minute == now.minute and alarm_time_second == now.second:
          alarm.start()
          
           
    
