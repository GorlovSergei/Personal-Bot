# Personal-Bot

Минимальная рабочая сборка для запуска на VPS.

## Локально
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
copy .env.example .env
PYTHONPATH=src python -m personal_bot.healthcheck
PYTHONPATH=src python -m personal_bot.main
