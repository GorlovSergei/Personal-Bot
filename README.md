# Personal Bot

Простой Telegram-бот, который отвечает на вопросы с помощью API ИИ, присылает новости и погоду по расписанию, а также ведёт напоминания.

## Установка

1. Установите Python 3.9 или новее.
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

В файле `config.py` укажите токен Telegram-бота и ключи внешних сервисов.

```python
TELEGRAM_TOKEN = "ваш-токен"
OPENAI_API_KEY = "ваш-ключ"
NEWS_API_KEY = "ключ-новостей"
WEATHER_API_KEY = "ключ-погоды"
```

## Запуск

Запустите файл `bot.py`:

```bash
python bot.py
```

Бот будет работать в режиме polling и принимать сообщения.
