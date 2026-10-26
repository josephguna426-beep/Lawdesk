#!/usr/bin/env bash
set -euo pipefail
SRC="${1:?usage: restore.sh backups/crms_<timestamp>}"
export PGPASSWORD="${DB_PASSWORD:-crms}"
psql -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "${DB_USER:-crms}" "${DB_NAME:-crms}" < "$SRC/db.sql"
tar -xzf "$SRC/private_storage.tar.gz" -C backend
echo "Restored from $SRC"
