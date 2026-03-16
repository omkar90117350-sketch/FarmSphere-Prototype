"""
FarmSphere — Weather API Utility
Integrates with OpenWeatherMap. Falls back to demo data if key is missing.
"""
import requests
import math


def get_weather_data(city: str, api_key: str) -> dict | None:
    """Fetch current weather from OpenWeatherMap."""
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        d = r.json()
        m = d["main"]
        # dew point approximation
        a, b = 17.27, 237.7
        try:
            alpha = ((a * m["temp"]) / (b + m["temp"])) + math.log(m["humidity"] / 100.0)
            dew = round((b * alpha) / (a - alpha))
        except Exception:
            dew = m["temp"] - 2
        return {
            "city":        d.get("name", city),
            "temperature": round(m["temp"]),
            "feels_like":  round(m["feels_like"]),
            "humidity":    m["humidity"],
            "wind_speed":  round(d["wind"]["speed"] * 3.6, 1),
            "pressure":    m["pressure"],
            "visibility":  round(d.get("visibility", 10000) / 1000, 1),
            "condition":   d["weather"][0]["description"].title(),
            "icon":        d["weather"][0]["icon"],
            "dew_point":   dew,
            "country":     d["sys"]["country"],
        }
    except Exception:
        return None


def get_forecast_data(city: str, api_key: str) -> list | None:
    """Fetch 7-day forecast (3-hour intervals → daily summary)."""
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        items = r.json().get("list", [])
        daily: dict = {}
        for item in items:
            day = item["dt_txt"].split(" ")[0]
            if day not in daily:
                daily[day] = {"temps": [], "icons": [], "rain": 0, "desc": ""}
            daily[day]["temps"].append(item["main"]["temp"])
            daily[day]["icons"].append(item["weather"][0]["icon"])
            daily[day]["rain"] = max(daily[day]["rain"], item.get("pop", 0) * 100)
            daily[day]["desc"] = item["weather"][0]["description"].title()
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        result = []
        for i, (_, data) in enumerate(list(daily.items())[:7]):
            result.append({
                "day":              "Today" if i == 0 else day_labels[i % 7],
                "high_temp":        round(max(data["temps"])),
                "low_temp":         round(min(data["temps"])),
                "condition":        data["desc"],
                "icon":             data["icons"][len(data["icons"]) // 2],
                "rain_probability": round(data["rain"]),
            })
        return result
    except Exception:
        return None
