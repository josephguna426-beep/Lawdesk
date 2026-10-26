# Proposed API Structure

| Group | Endpoints |
|-------|-----------|
| Auth | `GET /api/auth/csrf/`, `POST /api/auth/login/`, `POST /api/auth/logout/`, `GET /api/auth/me/` |
| Cases | `/api/cases/` (CRUD, `?q=&status=&court=&date_from=&date_to=`), `POST /api/cases/{id}/archive/` |
| Clients / Parties | `/api/clients/`, `/api/parties/` |
| Courts / Advocates | `/api/courts/`, `/api/advocates/` |
| Hearings | `/api/hearings/` (no delete), `POST /api/hearings/{id}/reschedule/`, `POST /api/hearings/{id}/cancel/` |
| Documents | `GET/POST /api/cases/{id}/documents/`, `GET /api/documents/{id}/download/` |
| Closure | `POST /api/cases/{id}/close/` |
| Closure PDFs | `GET/POST /api/cases/{id}/closure-pdfs/`, `POST /api/closure-pdfs/{id}/retry/`, `GET /api/closure-pdfs/{id}/download/` |
| Notifications | `/api/notifications/`, `POST /api/notifications/{id}/read/`, `POST /api/notifications/read-all/` |
| Dashboard | `GET /api/dashboard/` |
| Reports | `GET /api/reports/search/?q=`, `/api/reports/case-status/`, `/api/reports/upcoming-hearings/` |
| Audit | `GET /api/audit/` |
| Schema | `/api/schema/`, `/api/docs/` (Swagger UI) |
