#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${1:-/opt/personal-bot}"
echo "[post-check] APP_DIR=$APP_DIR"
systemctl status personal-bot --no-pager || true
echo "[post-check] done"
