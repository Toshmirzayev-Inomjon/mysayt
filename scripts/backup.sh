#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_DIR/backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
TIMESTAMP="$(date +%F_%H-%M-%S)"

mkdir -p "$BACKUP_DIR"

if [[ "${DJANGO_DB_ENGINE:-sqlite}" == "postgres" ]]; then
  : "${POSTGRES_DB:?POSTGRES_DB is required}"
  : "${POSTGRES_USER:?POSTGRES_USER is required}"
  : "${POSTGRES_HOST:?POSTGRES_HOST is required}"
  : "${POSTGRES_PORT:?POSTGRES_PORT is required}"
  PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_dump \
    -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" "$POSTGRES_DB" \
    > "$BACKUP_DIR/db_$TIMESTAMP.sql"
else
  cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/db_$TIMESTAMP.sqlite3"
fi

if [[ -d "$PROJECT_DIR/media" ]]; then
  tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" -C "$PROJECT_DIR" media
fi

find "$BACKUP_DIR" -type f -mtime +"$RETENTION_DAYS" -delete
