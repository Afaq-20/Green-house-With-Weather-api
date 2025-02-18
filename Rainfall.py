import requests
from datetime import datetime, timedelta

class WeatherDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_location_coordinates(self, city):
        """Get latitude and longitude for a city"""
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": city,
            "limit": 1,
            "appid": self.api_key
        }
        
        response = requests.get(geocoding_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"],
                    "name": data[0]["name"],
                    "country": data[0].get("country", "")
                }
        return None

    def get_current_weather(self, lat, lon):
        """Get current weather data"""
        weather_url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # Use metric units
        }
        
        response = requests.get(weather_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "rainfall": self._get_rainfall_data(data)
            }
        return None

    def _get_rainfall_data(self, weather_data):
        """Extract rainfall data from weather response"""
        rain_1h = 0
        if "rain" in weather_data:
            # Get last hour rainfall in mm
            rain_1h = weather_data["rain"].get("1h", 0)
        return rain_1h

def get_weather_for_city(city, api_key):
    """Helper function to get weather data for a city"""
    weather_fetcher = WeatherDataFetcher(api_key)
    
    # Get coordinates for the city
    location = weather_fetcher.get_location_coordinates(city)
    if not location:
        return None, f"Could not find coordinates for city: {city}"
    
    # Get weather data
    weather_data = weather_fetcher.get_current_weather(location["lat"], location["lon"])
    if not weather_data:
        return None, f"Could not fetch weather data for {city}"
    
    weather_data["city"] = location["name"]
    weather_data["country"] = location["country"]
    return weather_data, None

API_KEY = "ce8d768311942a293f8db60db6c52c5e"
CITY = "Lahore"

weather_data, error = get_weather_for_city(CITY, API_KEY)
if error:
    print(error)
else:
    print(f"Weather in {weather_data['city']}, {weather_data['country']}:")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Rainfall: {weather_data['rainfall']} mm")