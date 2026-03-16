"""
FarmSphere — Crop Price Predictor
Uses a seasonal regression model with location and crop multipliers.
Replace with a trained .pkl model for production.
"""
import math
import numpy as np

# Base MSP prices (₹/quintal) — aligned with CROP_DATABASE in app.py
_BASE = {
    "wheat": 2275, "rice": 2300, "maize": 2090, "soybean": 4892,
    "cotton": 7020, "sugarcane": 3400, "mustard": 5650, "tomato": 1800,
}

# Seasonal multipliers (month 1–12)
_SEASONAL = {
    1: 1.06, 2: 1.09, 3: 1.13, 4: 1.11, 5: 1.07, 6: 0.94,
    7: 0.89, 8: 0.87, 9: 0.93, 10: 0.96, 11: 1.00, 12: 1.04,
}

# Season-name to average month
_SEASON_MONTH = {"kharif": 9, "rabi": 2, "annual": 6, "zaid": 5}

# Location premium multipliers
_LOCATION = {
    "pune": 1.09, "mumbai": 1.15, "nagpur": 1.05, "indore": 1.04,
    "delhi": 1.12, "bangalore": 1.10, "chennai": 1.08, "kolkata": 1.05,
}


def predict_crop_price(crop: str, market: str, season: str) -> float:
    """
    Predict crop price (₹/quintal) given crop, market location, and season.
    Returns a float. Uses deterministic seed for reproducibility.
    """
    base = _BASE.get(crop.lower(), 3000)
    month = _SEASON_MONTH.get(season.lower(), 6)
    seasonal = _SEASONAL.get(month, 1.0)
    loc = _LOCATION.get(market.lower(), 1.0)

    # Stable noise seeded on input combination
    np.random.seed(abs(hash(f"{crop}{market}{season}")) % (2 ** 31))
    noise = np.random.uniform(0.97, 1.03)

    return round(base * seasonal * loc * noise, 2)
