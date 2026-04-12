#!/usr/bin/env bash
set -euo pipefail
latest="$(ls -1t backups/*.sqlite3 2>/dev/null | head -n1 || true)"
if [ -z "$latest" ]; then echo "backup stale: none"; exit 1; fi
echo "backup fresh: $latest"
