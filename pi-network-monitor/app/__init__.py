# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Try to load config.py, fallback to config_template.py
    if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'config.py')):
        app.config.from_object('config.Config')
    else:
        app.config.from_object('config_template.Config')

    db.init_app(app)

    with app.app_context():
        from app import routes, models
        db.create_all()

    return app
