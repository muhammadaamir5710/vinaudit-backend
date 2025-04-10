from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app) 
    
    db.init_app(app)
    
    from app.controllers.vehicle_controller import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix='/api')
    
    return app