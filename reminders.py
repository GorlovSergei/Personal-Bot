"""Простейшее хранилище напоминаний на базе JSON-файла."""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from config import REMINDERS_FILE


@dataclass
class Reminder:
    id: int
    text: str
    time: datetime


def load_reminders() -> List[Reminder]:
    path = Path(REMINDERS_FILE)
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return [Reminder(id=r["id"], text=r["text"], time=datetime.fromisoformat(r["time"])) for r in data]


def save_reminders(reminders: List[Reminder]) -> None:
    path = Path(REMINDERS_FILE)
    data = [asdict(r) | {"time": r.time.isoformat()} for r in reminders]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def add_reminder(text: str, time: datetime) -> Reminder:
    reminders = load_reminders()
    next_id = max((r.id for r in reminders), default=0) + 1
    reminder = Reminder(id=next_id, text=text, time=time)
    reminders.append(reminder)
    save_reminders(reminders)
    return reminder


def list_reminders() -> List[Reminder]:
    return load_reminders()


def remove_reminder(reminder_id: int) -> bool:
    reminders = load_reminders()
    new_list = [r for r in reminders if r.id != reminder_id]
    if len(new_list) == len(reminders):
        return False
    save_reminders(new_list)
    return True
