# Court Records Management System (CRMS)

React + Vite + TypeScript  |  Django REST Framework  |  PostgreSQL  |  Celery + Redis

One-month delivery plan, 6 sprints, 2 developers. See `docs/` for module map, sprint plan and API list.

## Folder overview

```
crms/
├── backend/     Django + DRF project (one app per module)
├── frontend/    React + Vite + TypeScript SPA (one feature folder per module)
├── docs/        Module map, sprints, API structure, backup/restore
├── postman/     Postman collection
├── scripts/     Backup / restore helpers
└── docker-compose.yml   PostgreSQL + Redis for local dev
```

## Quick start

```bash
# 1. services
docker compose up -d

# 2. backend
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations accounts courts parties cases hearings documents closures notifications audit
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver                              # http://localhost:8000
# Swagger UI: http://localhost:8000/api/docs/

# 3. background workers (separate terminals, from backend/)
celery -A config worker -l info
celery -A config beat -l info

# 4. frontend
cd frontend
npm install
npm run dev                                             # http://localhost:5173
```

## Notes
- Uses Django's built-in user model (no custom password table).
- Closure PDF is an application-generated summary, not an official court order.
- Documents and PDFs live in `backend/private_storage/` and are served only through authorised endpoints.
- Timezone: Asia/Kolkata (reminders: day-before 09:00, hearing-day 08:00).
