# app/models.py
from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    downtime_duration = db.Column(db.Integer, nullable=True)  # in seconds (nullable)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_interval_seconds = db.Column(db.Integer, default=4)
    timezone = db.Column(db.String(64), default='America/Los_Angeles')
    city = db.Column(db.String(128), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    last_weather_update = db.Column(db.DateTime, nullable=True)

class WeatherLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    temperature_f = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(64), nullable=False)
