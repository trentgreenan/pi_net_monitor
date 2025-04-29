# config_template.py

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/monitor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Weather API Settings
    WEATHER_API_KEY = 'your_openweathermap_api_key_here'
    WEATHER_UPDATE_INTERVAL_MINUTES = 30
    WEATHER_UNITS = 'imperial'
    PUBLIC_IP_LOOKUP_URL = 'https://api.ipify.org'
    GEOLOCATION_API_URL = 'http://ip-api.com/json/'
