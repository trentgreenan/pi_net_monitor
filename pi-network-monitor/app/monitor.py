# app/monitor.py
import os
import time
import subprocess
import requests
from datetime import datetime, timedelta
import pytz
from ping3 import ping
from app import db
from app.models import Event, Setting, WeatherLog
from config import Config
import logging

PACIFIC = pytz.timezone('America/Los_Angeles')
NETWORK_INTERFACE = "eth0"
CHECK_INTERVAL = 4  # seconds

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def is_eth_connected():
    try:
        with open(f"/sys/class/net/{NETWORK_INTERFACE}/carrier") as f:
            return f.read().strip() == '1'
    except Exception as e:
        logging.error(f"Ethernet check failed: {e}")
        return False

def is_reachable(ip):
    try:
        return ping(ip, timeout=1) is not None
    except:
        return False

def current_time():
    return datetime.now(PACIFIC)

def log_event(status):
    e = Event(timestamp=current_time(), status=status)
    db.session.add(e)
    db.session.commit()
    logging.info(f"Logged event: {status}")

def log_weather(city, temp_f, condition):
    w = WeatherLog(timestamp=current_time(), city=city, temperature_f=temp_f, condition=condition)
    db.session.add(w)
    db.session.commit()
    logging.info(f"Logged weather: {city}, {temp_f}°F, {condition}")

def get_or_create_setting():
    setting = Setting.query.first()
    if not setting:
        setting = Setting()
        db.session.add(setting)
        db.session.commit()
    return setting

def fetch_geolocation():
    """Use public IP to get city, lat, lon"""
    try:
        ip = requests.get(Config.PUBLIC_IP_LOOKUP_URL).text.strip()
        geo = requests.get(Config.GEOLOCATION_API_URL + ip).json()
        return geo["city"], float(geo["lat"]), float(geo["lon"])
    except Exception as e:
        logging.error(f"Geolocation lookup failed: {e}")
        return None, None, None

def fetch_weather(lat, lon):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&units={Config.WEATHER_UNITS}&appid={Config.WEATHER_API_KEY}"
        )
        r = requests.get(url)
        data = r.json()
        temp = data['main']['temp']
        condition = data['weather'][0]['main']
        return temp, condition
    except Exception as e:
        logging.error(f"Weather fetch failed: {e}")
        return None, None

def monitor_loop():
    logging.info("Starting monitoring loop...")
    last_status = None
    consecutive_failures = 0
    weather_timer = datetime.min

    while True:
        setting = get_or_create_setting()

        # Step 1: Run weather fetch every 30 minutes
        if not setting.city or not setting.latitude or not setting.longitude:
            city, lat, lon = fetch_geolocation()
            if city and lat and lon:
                setting.city = city
                setting.latitude = lat
                setting.longitude = lon
                db.session.commit()
                logging.info(f"Geolocation set: {city}, {lat}, {lon}")
        elif datetime.now() > (setting.last_weather_update or datetime.min) + timedelta(minutes=Config.WEATHER_UPDATE_INTERVAL_MINUTES):
            temp, condition = fetch_weather(setting.latitude, setting.longitude)
            if temp and condition:
                log_weather(setting.city, temp, condition)
                setting.last_weather_update = datetime.now()
                db.session.commit()

        # Step 2: Check Ethernet status
        if not is_eth_connected():
            if last_status != "ethernet_unplugged":
                log_event("ethernet_unplugged")
                last_status = "ethernet_unplugged"
            time.sleep(CHECK_INTERVAL)
            continue

        # Step 3: Check LAN & Internet
        lan_ok = is_reachable("192.168.1.1")
        internet_ok = any(is_reachable(ip) for ip in ["1.1.1.1", "8.8.8.8"])

        if lan_ok:
            if internet_ok:
                if last_status != "up":
                    log_event("up")
                    last_status = "up"
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                if consecutive_failures >= 2 and last_status != "internet_down":
                    log_event("internet_down")
                    last_status = "internet_down"
        else:
            if last_status != "network_down":
                log_event("network_down")
                last_status = "network_down"

        time.sleep(CHECK_INTERVAL)
