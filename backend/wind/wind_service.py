import requests
from typing import Dict

def validate_lat_lon(lat: float, lon: float):
    """
    Raises ValueError if latitude or longitude are out of valid range.
    """
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude {lat} out of range (-90 to 90)")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude {lon} out of range (-180 to 180)")

def fetch_open_meteo_wind(lat: float, lon: float) -> Dict:
    """
    Fetch current wind speed and direction from Open-Meteo for the given latitude and longitude.
    Returns a dict: {"speed": float or None, "direction": float or None}
    Raises ValueError if coordinates are invalid.
    """
    validate_lat_lon(lat, lon)
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data.get("current_weather", {})
    return {
        "speed": current.get("windspeed"),
        "direction": current.get("winddirection")
    }

def fetch_open_meteo_historical_wind(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    """
    Fetch historical wind data from Open-Meteo for the given lat/lon and date range.
    Dates should be in 'YYYY-MM-DD' format.
    Returns the full JSON response (contains hourly windspeed_10m and winddirection_10m).
    Raises ValueError if coordinates are invalid.
    """
    validate_lat_lon(lat, lon)
    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=windspeed_10m,winddirection_10m"
    )
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()

def parse_historical_wind(response: dict) -> dict:
    """
    Parse Open-Meteo historical API response to extract windspeed and winddirection arrays.
    Returns a dict: {"windspeed_10m": [...], "winddirection_10m": [...], "time": [...]}
    """
    hourly = response.get("hourly", {})
    return {
        "windspeed_10m": hourly.get("windspeed_10m", []),
        "winddirection_10m": hourly.get("winddirection_10m", []),
        "time": hourly.get("time", [])
    }
