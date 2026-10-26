# Backup and Restore

Back up **both** the database and `backend/private_storage/` (documents + closure PDFs).

```bash
./scripts/backup.sh            # creates backups/crms_<timestamp>/
./scripts/restore.sh backups/crms_<timestamp>
```

Test a restore on a scratch database periodically (Sprint 6 acceptance item).
Never commit backups or `.env` files.
