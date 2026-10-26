# Module Map

| # | Module | Backend app (`backend/apps/`) | Frontend feature (`frontend/src/features/`) | Owner |
|---|--------|------------------------------|---------------------------------------------|-------|
| 1 | Authentication and Access Control | `accounts` | `auth` | Person 1 |
| 2 | Dashboard | `dashboard` | `dashboard` | Person 1 |
| 3 | Case Records Management | `cases` | `cases` | Person 1 |
| 4 | Client and Parties Management | `parties` | `clients`, `parties` | Person 2 |
| 5 | Court and Advocate Management | `courts` | `courts`, `advocates` | Person 2 |
| 6 | Hearing and Proceedings Management | `hearings` | `hearings` | Person 2 |
| 7 | Document Management | `documents` | `documents` | Person 1 (API) / Person 2 (UI) |
| 8 | Case Closure and Closure PDF | `closures` | `closures` | Person 1 |
| 9 | Hearing Reminders and Notifications | `notifications` | `notifications` | Person 2 |
| 10 | Reports and Search | `reports` | `reports` | Person 2 |
| 11 | Settings, Audit and Backup | `audit` | `settings` | Person 2 (UI) / Person 1 (audit hooks) |

Shared helpers: `backend/apps/common/`, `frontend/src/components/`, `frontend/src/lib/`.

Each module has six tasks (see the project documentation). Track them as
Not Started / In Progress / Blocked / Done on one shared board.
