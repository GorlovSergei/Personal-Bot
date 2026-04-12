#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
cp data/personal_bot.sqlite3 "backups/personal_bot_$(date +%F_%H-%M-%S).sqlite3" 2>/dev/null || true
echo "backup done"
