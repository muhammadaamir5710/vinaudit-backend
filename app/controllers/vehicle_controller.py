from flask import Blueprint, jsonify, request
from app.services.vehicle_service import VehicleService
from typing import Tuple, Dict, Any

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/search", methods=["GET"])
def search() -> Tuple[Dict[str, Any], int]:
    """
    Search for vehicle valuations with additional factors
    ---
    parameters:
      - name: year
        in: query
        type: integer
        required: true
      - name: make
        in: query
        type: string
        required: true
      - name: model
        in: query
        type: string
        required: true
      - name: mileage
        in: query
        type: integer
        required: false
      - name: trim
        in: query
        type: string
        required: false
      - name: body_type
        in: query
        type: string
        required: false
      - name: state
        in: query
        type: string
        required: false
    responses:
      200:
        description: Vehicle valuation result
      400:
        description: Missing or invalid parameters
      500:
        description: Internal server error
    """
    year = request.args.get("year")
    make = request.args.get("make")
    model = request.args.get("model")
    mileage = request.args.get("mileage", None)
    trim = request.args.get("trim", None)
    color = request.args.get("color", None)
    state = request.args.get("dealer_state", None)

    if not all([year, make, model]):
        return {"error": "Missing required parameters (year, make, model)"}, 400

    try:
        year = int(year)
        if mileage:
            mileage = int(mileage)
    except ValueError:
        return {"error": "Year and mileage must be integers"}, 400

    try:
        result = VehicleService.calculate_market_value(
            year, make, model, mileage, trim, color, state
        )
        return jsonify(result), 200
    except Exception as e:
        return {"error": str(e)}, 500


@vehicle_bp.route("/makes-models", methods=["GET"])
def get_makes_and_models() -> Tuple[Dict[str, Any], int]:
    """
    Get available makes and models
    ---
    responses:
      200:
        description: Dictionary of years with makes and models
      500:
        description: Internal server error
    """
    try:
        data = VehicleService.get_makes_and_models()
        return jsonify(data), 200
    except Exception as e:
        return {"error": str(e)}, 500
