import requests
import json
import datetime
# from app.models.data_models import WeatherModel
from pydantic import BaseModel
class WeatherModel(BaseModel):
    date: str
    high_temp: int
    low_temp: int
    forecast: str
    
class WeatherService:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long

    def get_weather_forecast_url(self):
        # NWS requires a User-Agent
        
        headers = {
            'User-Agent': '(weather-app, contact@example.com)',
            'Accept': 'application/geo+json'
        }
        url = f"https://api.weather.gov/points/{self.lat},{self.long}"    
        try:
            print(f"Fetching weather url from: {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            properties = data.get('properties', {})
            
            weather_url = properties.get('forecastHourly', '')
            print(f"Hourly forecast URL: {weather_url}")
            return weather_url
        
        except Exception as e:
            print(f"Error: {e}")

    
    def get_weather_data(self):
        weather_url = self.get_weather_forecast_url()
        if not weather_url:
            print("No weather URL found.")
            return
        
        response = requests.get(weather_url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        return data
        
    def get_weather_data_for_date(self, date, weather_data):
        """Fetches weather data for a specific date from the provided weather data."""
        
        day_data = []
        if not weather_data:
            print("No weather data provided.")
            return None
        
        properties = weather_data.get('properties', {})
        periods = properties.get('periods', [])
        
        for period in periods:
            start_time_str = period.get('startTime', '')
            start_time = datetime.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            
            if start_time.date() == date.date():
                day_data.append(period)
        
        if not day_data:
            print(f"No weather data found for date: {date.date()}")
            return None
        
        return day_data
        

    def get_temperature_for_day(self, day, weather_data=None):
        """Extracts temperature data for a specific day."""
        if not weather_data:
            return None
        
        temperatures = []
        for period in weather_data:
            temp = period.get('temperature', None)
            if temp is not None:
                temperatures.append(temp)
        
        return temperatures
    
    def find_max_min_temperature(self, day):
        """Finds the maximum and minimum temperatures for a specific day."""
        temperatures = self.get_temperature_for_day(day)
        if not temperatures:
            return None, None
        
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        
        return max_temp, min_temp
    
    
    
    
    
    
    
    
    
    
    # def get_weekly_forcast(self, today):
    #     """Fetches a 7-day weather forecast starting from today."""
    #     weather_data = self.get_weather_data()
    #     if not weather_data:
    #         return None
        
    #     properties = weather_data.get('properties', {})
    #     periods = properties.get('periods', [])
        
    #     weather_data = []
        
    #     for i in range(7):
    #         temps = []
    #         forecast = []
    #         day = today + datetime.timedelta(days=i)
    #         day_forecast = []
    #         for period in periods:
    #             date = period.get('startTime', '').split('T')[0]
    #             if date == day.strftime("%Y-%m-%d"):
    #                 temps.append(period.get('temperature', None))
    #                 day_forecast.append(period.get('shortForecast', ''))
    #             # print(period)
    #         weather = WeatherModel(
    #             date = day.strftime("%Y-%m-%d"),
    #             high_temp = max(temps) if temps else -100,
    #             low_temp = min(temps) if temps else -100,
    #             forecast = self.interperet_forecast(day_forecast)
                     
    #         )        
    #         # print(weather)
               
    #         weather_data.append(weather)
        
    #     return weather_data
    
    # def interperet_forecast(self, forecast: list) -> str:
    #     """Interprets the forecast string to a simplified description."""
    #     final = "Clear"
    #     for item in forecast:
    #         print(item)
    #         if "snow" in item.lower() or "blizzard" in item.lower() or "sleet" in item.lower():
    #             final = "Snow"

    #         elif "thunderstorm" in item.lower() or "storm" in item.lower() or "t-storm" in item.lower() and final != "Snow":
    #             final = "Storm"

    #         elif "rain" in item.lower() or "shower" in item.lower() or "drizzle" in item.lower() and final not in ["Snow", "Storm"]:
    #             final = "Rain"

    #         elif "fog" in item.lower() or "haze" in item.lower() or "smoke" in item.lower() and final not in ["Snow", "Storm", "Rain"]:
    #             final = "Foggy"

    #         elif "cloud" in item.lower() or "overcast" in item.lower() and final not in ["Snow", "Storm", "Rain", "Foggy"]:
    #             final = "Cloudy"

    #         elif "windy" in item.lower() or "breezy" in item.lower() and final not in ["Snow", "Storm", "Rain", "Foggy", "Cloudy"]:
    #             final = "Windy"
    #     print(f"Interpreted forecast: {final}")
    #     print("------------------")
    #     return final
            
if __name__ == "__main__":
    # Using your specific LWX coordinates
    lat = 38.99
    long = -77.01
    
    weather_service = WeatherService(lat, long)
    
    # Example: Get weather data for today
    today = datetime.datetime.now()
    weather_data = weather_service.get_weather_data()
    today_data = weather_service.get_weather_data_for_date(today, weather_data)
    today_weather = weather_service.get_temperature_for_day(today, today_data)
    print(f"Today's Weather: {today_weather}")
    # weather_service.get_weekly_forcast(today)
    