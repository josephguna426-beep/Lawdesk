#!/usr/bin/env bash
set -euo pipefail
STAMP=$(date +%Y%m%d_%H%M%S)
OUT="backups/crms_${STAMP}"
mkdir -p "$OUT"
export PGPASSWORD="${DB_PASSWORD:-crms}"
pg_dump -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "${DB_USER:-crms}" "${DB_NAME:-crms}" > "$OUT/db.sql"
tar -czf "$OUT/private_storage.tar.gz" -C backend private_storage
echo "Backup written to $OUT"
