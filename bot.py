"""Основной файл Telegram-бота."""

import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import openai
from config import TELEGRAM_TOKEN, OPENAI_API_KEY, CHAT_ID
from news import get_news
from weather import get_weather
from reminders import add_reminder, list_reminders, remove_reminder
from voice_recognition import voice_to_text

logging.basicConfig(level=logging.INFO)

openai.api_key = OPENAI_API_KEY

scheduler = AsyncIOScheduler()

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я персональный бот. Спроси меня о чём угодно."
    )


async def ask_ai(text: str) -> str:
    if not OPENAI_API_KEY:
        return "API ключ OpenAI не настроен"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        return f"Ошибка обращения к ИИ: {exc}"


async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = await ask_ai(text)
    await update.message.reply_text(reply)


async def handle_voice(update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    path = "voice.ogg"
    await file.download_to_drive(path)
    text = voice_to_text(path)
    await update.message.reply_text(f"Распознано: {text}")


async def remind_command(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date_str = context.args[0] + " " + context.args[1]
        text = " ".join(context.args[2:])
        remind_time = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Использование: /remind DD.MM.YYYY HH:MM текст"
        )
        return

    reminder = add_reminder(text, remind_time)
    scheduler.add_job(
        send_reminder,
        "date",
        run_date=remind_time,
        args=(update.message.chat_id, reminder.id, reminder.text),
    )
    await update.message.reply_text(f"Напоминание сохранено с id {reminder.id}")


async def send_reminder(chat_id: int, reminder_id: int, text: str):
    await app.bot.send_message(chat_id=chat_id, text=f"Напоминание: {text}")
    remove_reminder(reminder_id)


def schedule_daily():
    scheduler.add_job(
        send_daily_news,
        "cron",
        hour=8,
    )
    scheduler.add_job(
        send_daily_weather,
        "cron",
        hour=7,
    )
    scheduler.start()


async def send_daily_news():
    # Здесь можно указать ID вашего чата или реализовать подписку пользователей
    # Для примера используется одно значение
    chat_id = CHAT_ID
    news = get_news()
    await app.bot.send_message(chat_id=chat_id, text=news)


async def send_daily_weather():
    chat_id = CHAT_ID
    weather = get_weather()
    await app.bot.send_message(chat_id=chat_id, text=weather)


async def list_command(update, context):
    reminders = list_reminders()
    if not reminders:
        await update.message.reply_text("Напоминаний нет")
    else:
        lines = [f"{r.id}: {r.text} ({r.time:%d.%m.%Y %H:%M})" for r in reminders]
        await update.message.reply_text("\n".join(lines))


async def delete_command(update, context):
    try:
        reminder_id = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /deletereminder ID")
        return
    if remove_reminder(reminder_id):
        await update.message.reply_text("Удалено")
    else:
        await update.message.reply_text("Не найдено")


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("remind", remind_command))
app.add_handler(CommandHandler("listreminders", list_command))
app.add_handler(CommandHandler("deletereminder", delete_command))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

schedule_daily()

if __name__ == "__main__":
    app.run_polling()
