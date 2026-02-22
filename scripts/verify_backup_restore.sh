#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_DIR/backups}"

mkdir -p "$BACKUP_DIR"

"$PROJECT_DIR/scripts/backup.sh"

LATEST_SQL="$(ls -1t "$BACKUP_DIR"/*.sql 2>/dev/null | head -n1 || true)"
LATEST_SQLITE="$(ls -1t "$BACKUP_DIR"/*.sqlite3 2>/dev/null | head -n1 || true)"

if [[ -n "$LATEST_SQL" ]]; then
  echo "Testing restore from SQL backup: $LATEST_SQL"
  "$PROJECT_DIR/scripts/restore.sh" "$LATEST_SQL"
elif [[ -n "$LATEST_SQLITE" ]]; then
  echo "Testing restore from SQLite backup: $LATEST_SQLITE"
  "$PROJECT_DIR/scripts/restore.sh" "$LATEST_SQLITE"
else
  echo "Backup file topilmadi."
  exit 1
fi

echo "Backup-restore verification finished."
