#!/usr/bin/env bash
set -euo pipefail
latest="$(ls -1t backups/*.sqlite3 2>/dev/null | head -n1 || true)"
if [ -z "$latest" ]; then echo "no backups"; exit 1; fi
cp "$latest" data/personal_bot.sqlite3
echo "restored: $latest"
