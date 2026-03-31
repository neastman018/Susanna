""""Class for Handling the Alarm Service logic."""
import json
from datetime import datetime, timedelta
from typing import List
import pygame
from colorama import Fore, Style

from app.services.data_service import DataService
from app.models.data_models import AlarmModel
from app.services.application_state_service import ASService

path_to_sounds = "public/sounds/"

class AlarmService:
    def __init__(self, data_service: DataService, as_service: ASService, last_played_min=0, backup="Thats_Life.mp3"):       
        pygame.mixer.init()
        self.last_played_min = last_played_min
        self.backup = f"{path_to_sounds}{backup}"
        self.data_service = data_service
        self.as_service = as_service
        print(f"Alarm is ready")


    def find_todays_alarms(self, today) -> List[AlarmModel]:
        """Finds and returns alarms scheduled for today."""
        alarms = self.data_service.grab_all_alarms()
        todays_alarms = []
        
        for alarm in alarms:
            if alarm.start_date <= str(today):
                if alarm.repeat == "Once":
                    if alarm.start_date == str(today):
                        todays_alarms.append(alarm)
                elif alarm.repeat == "Daily":
                    todays_alarms.append(alarm)
                elif alarm.repeat == "Weekly":
                    if today.strftime("%A") in alarm.day_of_week:
                        todays_alarms.append(alarm)
                elif alarm.repeat == "Monthly":
                    if int(alarm.start_date.split("-")[2]) == today.day:
                        todays_alarms.append(alarm)
                elif alarm.repeat == "Yearly":
                    if alarm.start_date[5:] == str(today)[5:]:
                        todays_alarms.append(alarm)
    
        return todays_alarms
    
    def find_tomorrows_alarms(self, today) -> List[AlarmModel]:
        """Finds and returns alarms scheduled for today."""
        alarms = self.data_service.grab_all_alarms()
        tomorrows_alarms = []
        tomorrow = today + timedelta(days=1)
        for alarm in alarms:
            if alarm.start_date <= str(tomorrow):
                if alarm.repeat == "Once":
                    if alarm.start_date == str(tomorrow):
                        tomorrows_alarms.append(alarm)
                elif alarm.repeat == "Daily":
                    tomorrows_alarms.append(alarm)
                elif alarm.repeat == "Weekly":
                    if tomorrow.strftime("%A") in alarm.day_of_week:
                        tomorrows_alarms.append(alarm)
                elif alarm.repeat == "Monthly":
                    if int(alarm.start_date.split("-")[2]) == tomorrow.day:
                        tomorrows_alarms.append(alarm)
                elif alarm.repeat == "Yearly":
                    if alarm.start_date[5:] == str(tomorrow)[5:]:
                        tomorrows_alarms.append(alarm) 
        
        return tomorrows_alarms
        
    def find_next_alarm(self, today, time):
        """Loads alarms scheduled for today."""
        todays_alarms = self.find_todays_alarms(today)
        # print("Today's Alarms:", todays_alarms)
        
        if not todays_alarms:
            return None
        
        next_alarm = None
        
        for alarm in todays_alarms:
            alarm_time = datetime.strptime(alarm.alarm_time, "%H:%M").time()
            
            if alarm_time > datetime.strptime(f"{time.hour}:{time.minute}", "%H:%M").time():
                if next_alarm is None or alarm_time < datetime.strptime(next_alarm.alarm_time, "%H:%M").time():
                    next_alarm = alarm
        
        if next_alarm is None:
            tomorrows_alarms = self.find_tomorrows_alarms(today)
            # print("Tomorrow's Alarms:", tomorrows_alarms)
            if not tomorrows_alarms:
                return None
            for alarm in tomorrows_alarms:
                alarm_time = datetime.strptime(alarm.alarm_time, "%H:%M").time()
                if next_alarm is None or alarm_time < datetime.strptime(next_alarm.alarm_time, "%H:%M").time():
                    next_alarm = alarm
                              
        return next_alarm
    
    def is_active(self) -> bool:
        # Checks if the music is currently playing
        return pygame.mixer.music.get_busy()
    
    def play_alarm(self, alarm_sound):
        if alarm_sound and not self.is_active():
            try: 
                pygame.mixer.music.load(alarm_sound)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing alarm: {e} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                print(f"playing backup file")
                pygame.mixer.music.load(self.backup)
                pygame.mixer.music.play()
        else:
            print(f"Alarm sound not initialized. ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
            # log("Attempted to play alarm without initializing sound.")
            
    def activate(self, current_time, hour, minute, alarm_sound) -> bool:
        # print(f"{Fore.GREEN}{hour == current_time.hour}{Style.RESET_ALL}")
        # print(f"{Fore.GREEN}{minute == current_time.minute}{Style.RESET_ALL}")
        # print(f"{Fore.GREEN}{not self.is_active()}{Style.RESET_ALL}")
        # print(f"{Fore.GREEN}{current_time.minute != self.last_played_min}{Style.RESET_ALL}")
        
        if (
            hour == current_time.hour
            and minute == current_time.minute
            and not self.is_active()
            and current_time.minute != self.last_played_min
        ):
            print(f"{Fore.BLUE}Playing the Alarm!{Style.RESET_ALL}")
            self.play_alarm(alarm_sound)
            self.last_played_min = current_time.minute

    def alarm_stop(self) -> bool:
        if self.is_active():
            pygame.mixer.music.stop()
            # log("Alarm stopped")
            
    def activate_next_alarm(self, current_time) -> int:
        today = current_time.date()
        next_alarm = self.find_next_alarm(today, current_time.time())
        
        if not next_alarm:
            print(f"No alarms set for the rest of today. ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
            return 0
        else:
            # print("Next Alarm:", next_alarm)
            alarm_sound = f"{path_to_sounds}{next_alarm.sound}"
            alarm_hour = int(next_alarm.alarm_time.split(":")[0])
            alarm_minute = int(next_alarm.alarm_time.split(":")[1])
            
            print(f"{Fore.GREEN}Checking alarm for {alarm_hour}:{alarm_minute} with sound {alarm_sound}{Style.RESET_ALL}")

            self.activate(current_time, alarm_hour, alarm_minute, alarm_sound)
            return 1
