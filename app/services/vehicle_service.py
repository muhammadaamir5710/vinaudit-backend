from datetime import datetime
from typing import Dict, List, Optional
from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:
    """Business logic for vehicle valuation"""

    @staticmethod
    def calculate_market_value(
        year: int,
        make: str,
        model: str,
        mileage: int = None,
        trim: Optional[str] = None,
        color: Optional[str] = None,
        dealer_state: Optional[str] = None,
    ) -> Dict:
        """
        Calculate market value with mileage adjustment
        Returns: {
            'estimate': formatted_price,
            'listings': [vehicle_dicts],
            'calculation_date': iso_date_string
        }
        """
        filters = {
            "year": year,
            "make": make,
            "model": model,
            "trim": trim,
            "color": color,
            "dealer_state": dealer_state,
            "mileage": mileage,
        }

        
        avg_price = VehicleRepository.get_average_price_with_filters(filters)

        if avg_price:
            if mileage:
                avg_price = VehicleService._adjust_for_mileage(avg_price, mileage, year)
            if trim:
                avg_price = VehicleService._adjust_for_trim(avg_price, trim)
            if color:                
                avg_price = VehicleService._adjust_for_body_color(avg_price, color)
            if dealer_state:
                avg_price = VehicleService._adjust_for_state(avg_price, dealer_state)

        listings = VehicleRepository.get_listings_with_filters(filters)

        return {
            "estimate": VehicleService._format_price(avg_price) if avg_price else "N/A",
            "listings": [vehicle.to_dict() for vehicle in listings],
            "calculation_date": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_makes_and_models() -> Dict[int, Dict[str, List[str]]]:
        """Get all available years with makes and models"""
        result = {}
        current_year = datetime.now().year

        years = range(1990, current_year + 1)

        for year in years:
            makes = VehicleRepository.get_makes_by_year(year)
            make_models = {}

            for make in makes:
                models = VehicleRepository.get_models_by_make_year(year, make)
                make_models[make] = models

            if make_models:
                result[year] = make_models

        return result

    @staticmethod
    def _adjust_for_mileage(base_price: float, mileage: int, year: int) -> float:
        """Apply non-linear mileage adjustment"""
        current_year = datetime.now().year
        vehicle_age = current_year - year

        base_depreciation = 0.10  # 10% per year

        avg_miles_per_year = 12000
        expected_miles = vehicle_age * avg_miles_per_year
        mileage_diff = mileage - expected_miles

        if mileage_diff > 0:
            adjustment_factor = 0.15 + (mileage_diff / 100000 * 0.05)
            adjustment = mileage_diff * adjustment_factor
        else:
            adjustment = mileage_diff * 0.08

        adjusted_price = base_price - adjustment

        return max(adjusted_price, base_price * 0.3)
    
    
    @staticmethod
    def _adjust_for_trim(price: float, trim: str) -> float:
        trim = trim.lower()
        premium_trims = ["limited", "platinum", "sport", "titanium", "premium", "xlt", "lariat"]
        budget_trims = ["base", "s", "lx", "le"]

        if any(keyword in trim for keyword in premium_trims):
            price *= 1.10
        elif any(keyword in trim for keyword in budget_trims):
            price *= 0.95
        return price


    @staticmethod
    def _adjust_for_body_color(price: float, body_color: str) -> float:
        body_color = body_color.lower()
        if body_color in ["black", "white", "silver", "gray"]:
            return price * 1.08
        elif body_color in ["wind chill pearl", "ice cap", "red"]:
            return price * 0.97
        return price


    @staticmethod
    def _adjust_for_state(price: float, state: str) -> float:
        state = state.upper()
        high_cost_states = {"CA": 1.20, "NY": 1.08, "WA": 1.07}
        low_cost_states = {"TX": 0.97, "OH": 0.95, "MI": 0.93}

        if state in high_cost_states:
            return price * high_cost_states[state]
        elif state in low_cost_states:
            return price * low_cost_states[state]
        return price


    @staticmethod
    def _format_price(price: float) -> str:
        """Format price as currency rounded to nearest $100"""
        rounded = round(price / 100) * 100
        return f"${rounded:,.0f}"
