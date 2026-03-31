from pydantic import BaseModel

class QuoteModel(BaseModel):
    quote: str
    author: str
    
class AlarmModel(BaseModel):
    alarm_time: str
    start_date: str
    repeat: str
    day_of_week: list[str]
    sound: str
    label: str
    armed: bool # Remember an unauthorized armed alarm is a terror attack to sleeping roommates

class WeatherModel(BaseModel):
    date: str
    high_temp: int
    low_temp: int
    forecast: str
    chance_of_precipitation: int
    
    
ConfigModel = {
    "ALARM": {
        "ALARM_SOUND": "Thats_Life.mp3",
        "WAKE_UP_TIMES": {
            "SUNDAY": "7:00",
            "MONDAY": "5:30",
            "TUESDAY": "5:30",
            "WEDNESDAY": "5:30",
            "THURSDAY": "5:30",
            "FRIDAY": "5:30",
            "SATURDAY": "7:00"
        }
    },
    "WEATHER": {
        "LATITUDE": 38.93368707829988,
        "LONGITUDE": -77.1774930079404,
        "TODAY_HIGH": None,
        "TODAY_LOW": None,
    },
    "CALENDARS": {
        "PRIMARY": {
            "NAME": "Personal",
            "ICAL_URL": "https://calendar.google.com/calendar/ical/nick.eastman%40youthapostles.org/public/basic.ics"
        }
    },
    "WORDOFTHEDAY": {
        "WORD": None,
        "DEFINITION": None
    }
}