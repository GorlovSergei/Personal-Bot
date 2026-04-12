from __future__ import annotations
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from personal_bot.config import load_settings

dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message) -> None:
    await message.answer("Personal-bot запущен ✅")

async def main() -> None:
    settings = load_settings()
    bot = Bot(token=settings.bot_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
