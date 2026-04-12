from __future__ import annotations
import os
from pathlib import Path
from personal_bot.config import load_settings

def main() -> int:
    s = load_settings()
    Path(os.path.dirname(s.database_path) or ".").mkdir(parents=True, exist_ok=True)
    print("OK: config loaded, paths ready")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
