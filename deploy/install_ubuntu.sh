#!/usr/bin/env bash
set -euo pipefail
APP_DIR="/opt/personal-bot"
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
cd "$APP_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo cp deploy/personal-bot.service /etc/systemd/system/personal-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now personal-bot
echo "install done"
