"""Получение прогноза погоды из OpenWeatherMap."""

import requests
from config import WEATHER_API_KEY

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str = "Moscow") -> str:
    """Возвращает строку с текущей погодой."""
    if not WEATHER_API_KEY:
        return "API ключ погоды не настроен"

    params = {
        "appid": WEATHER_API_KEY,
        "q": city,
        "units": "metric",
        "lang": "ru",
    }
    try:
        resp = requests.get(WEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Погода в {city}: {temp}°C, {desc}"
    except Exception as exc:
        return f"Ошибка получения погоды: {exc}"
