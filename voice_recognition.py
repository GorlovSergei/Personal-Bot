"""Преобразование голосовых сообщений в текст."""

import os
from pydub import AudioSegment
import speech_recognition as sr


def voice_to_text(file_path: str) -> str:
    """Конвертирует аудиофайл в текст."""
    wav_path = os.path.splitext(file_path)[0] + ".wav"
    AudioSegment.from_file(file_path).export(wav_path, format="wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
    except Exception as exc:
        text = f"Ошибка распознавания: {exc}"
    finally:
        os.remove(wav_path)
    return text
