#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:8000}"
OUT_DIR="${2:-lighthouse-reports}"

mkdir -p "$OUT_DIR"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx topilmadi. Node.js o'rnatib qayta urinib ko'ring."
  exit 1
fi

npx --yes lighthouse "$URL" \
  --quiet \
  --chrome-flags='--headless' \
  --output html --output json \
  --output-path "$OUT_DIR/report"

echo "Lighthouse report created at: $OUT_DIR/report.html"
