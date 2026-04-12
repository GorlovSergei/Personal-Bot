test:
python -m unittest discover -s tests -v

health:
PYTHONPATH=src python -m personal_bot.healthcheck

backup:
bash scripts/backup_db.sh

restore_latest:
bash scripts/restore_db.sh

backup_check:
bash scripts/check_backup_freshness.sh
