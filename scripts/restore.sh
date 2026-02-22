#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup-file.sql|backup-file.sqlite3>"
  exit 1
fi

BACKUP_FILE="$1"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ "$BACKUP_FILE" == *.sql ]]; then
  : "${POSTGRES_DB:?POSTGRES_DB is required}"
  : "${POSTGRES_USER:?POSTGRES_USER is required}"
  : "${POSTGRES_HOST:?POSTGRES_HOST is required}"
  : "${POSTGRES_PORT:?POSTGRES_PORT is required}"
  PGPASSWORD="${POSTGRES_PASSWORD:-}" psql \
    -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" "$POSTGRES_DB" \
    < "$BACKUP_FILE"
else
  cp "$BACKUP_FILE" "$PROJECT_DIR/db.sqlite3"
fi
