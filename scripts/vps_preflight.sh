#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${1:-/opt/personal-bot}"
echo "[preflight] APP_DIR=$APP_DIR"
test -d "$APP_DIR"
test -f "$APP_DIR/.env"
echo "[preflight] ok"
