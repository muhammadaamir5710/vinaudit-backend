import json
from flask import url_for


def test_search_success(client, mock_vehicle_service):
    """Test successful search with required parameters"""
    mock_response = {
        "estimate": "$15,000",
        "listings": [
            {
                "year": 2015,
                "make": "Toyota",
                "model": "Camry",
                "price": 15000,
                "mileage": 80000,
                "location": "CA",
            }
        ],
        "calculation_date": "2023-01-01T00:00:00",
    }
    mock_vehicle_service.calculate_market_value.return_value = mock_response

    response = client.get(
        "/search", query_string={"year": "2015", "make": "Toyota", "model": "Camry"}
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["estimate"] == "$15,000"
    assert len(data["listings"]) == 1


def test_search_with_mileage(client, mock_vehicle_service):
    """Test search with mileage filter"""
    mock_vehicle_service.calculate_market_value.return_value = {
        "estimate": "$14,500",
        "listings": [],
        "calculation_date": "2023-01-01T00:00:00",
    }

    response = client.get(
        "/search",
        query_string={
            "year": "2015",
            "make": "Toyota",
            "model": "Camry",
            "mileage": "85000",
        },
    )

    assert response.status_code == 200


def test_search_with_trim(client, mock_vehicle_service):
    """Test search with trim filter"""
    mock_vehicle_service.calculate_market_value.return_value = {
        "estimate": "$16,000",
        "listings": [],
        "calculation_date": "2023-01-01T00:00:00",
    }

    response = client.get(
        "/search",
        query_string={"year": "2015", "make": "Toyota", "model": "Camry", "trim": "LE"},
    )

    assert response.status_code == 200


def test_search_missing_parameters(client):
    """Test search with missing required parameters"""
    response = client.get("/search")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Missing required parameters" in data["error"]


def test_search_invalid_year(client):
    """Test search with invalid year parameter"""
    response = client.get(
        "/search", query_string={"year": "invalid", "make": "Toyota", "model": "Camry"}
    )
    assert response.status_code == 400


def test_makes_models_endpoint(client, mock_vehicle_service):
    """Test makes and models endpoint"""
    mock_response = {2015: {"Toyota": ["Camry", "Corolla"]}}
    mock_vehicle_service.get_makes_and_models.return_value = mock_response

    response = client.get("/makes-models")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "2015" in data


def test_search_service_error(client, mock_vehicle_service):
    """Test error handling when service fails"""
    mock_vehicle_service.calculate_market_value.side_effect = Exception("Service error")

    response = client.get(
        "/search", query_string={"year": "2015", "make": "Toyota", "model": "Camry"}
    )
    assert response.status_code == 500
