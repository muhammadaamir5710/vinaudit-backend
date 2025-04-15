from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config
from flask_cors import CORS
from flask_caching import Cache

cache = Cache()
db = SQLAlchemy()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 3600 
    
    CORS(app) 
    
    db.init_app(app)
    cache.init_app(app)
    
    from app.controllers.vehicle_controller import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix='/api')
    
    return app