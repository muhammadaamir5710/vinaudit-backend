import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from app import db


@pytest.fixture(scope="module")
def app():
    """Create and configure a new Flask app for testing"""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.controllers.vehicle_controller import vehicle_bp

    app.register_blueprint(vehicle_bp)

    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def client(app):
    """Create test client within app context"""
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture(scope="function")
def mock_vehicle_service():
    """Mock the VehicleService"""
    with patch("app.controllers.vehicle_controller.VehicleService") as mock:
        yield mock


@pytest.fixture(scope="function")
def mock_vehicle_repo():
    """Mock the VehicleRepository"""
    with patch("app.services.vehicle_service.VehicleRepository") as mock:
        mock.get_average_price_with_filters.return_value = 18000
        mock.get_listings_with_filters.return_value = []
        mock.get_available_years.return_value = [2015, 2016]
        mock.get_makes_by_year.return_value = ["Toyota"]
        mock.get_models_by_make_year.return_value = ["Camry"]
        yield mock
