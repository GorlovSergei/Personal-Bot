from __future__ import annotations
import os
from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dotenv import load_dotenv

@dataclass(slots=True)
class Settings:
    bot_token: str
    openai_api_key: str
    timezone: str = "Europe/Moscow"
    database_path: str = "data/personal_bot.sqlite3"
    owner_chat_id: int | None = None

def load_settings() -> Settings:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    timezone = os.getenv("TZ", "Europe/Moscow")
    database_path = os.getenv("DATABASE_PATH", "data/personal_bot.sqlite3")
    owner_chat_id_raw = os.getenv("OWNER_CHAT_ID", "").strip()

    if not bot_token:
        raise ValueError("Не найден BOT_TOKEN")

    if owner_chat_id_raw:
        try:
            owner_chat_id = int(owner_chat_id_raw)
        except ValueError as exc:
            raise ValueError("OWNER_CHAT_ID должен быть целым числом") from exc
    else:
        owner_chat_id = None

    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Неизвестный TZ: {timezone}") from exc

    return Settings(
        bot_token=bot_token,
        openai_api_key=openai_api_key,
        timezone=timezone,
        database_path=database_path,
        owner_chat_id=owner_chat_id,
    )
