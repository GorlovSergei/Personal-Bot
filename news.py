"""Получение новостей с помощью NewsAPI."""

import requests
from config import NEWS_API_KEY

NEWS_URL = "https://newsapi.org/v2/top-headlines"


def get_news(country: str = "ru") -> str:
    """Возвращает строку с несколькими новостями."""
    if not NEWS_API_KEY:
        return "API ключ новостей не настроен"

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": 5,
    }
    try:
        resp = requests.get(NEWS_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        lines = [f"- {a['title']}" for a in articles]
        return "\n".join(lines) if lines else "Новости не найдены"
    except Exception as exc:
        return f"Ошибка получения новостей: {exc}"
