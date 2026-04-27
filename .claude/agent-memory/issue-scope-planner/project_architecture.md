---
name: Backend Architecture Overview
description: Core patterns for routes, CRUD, models, and tests in the full-stack-fastapi-template
type: project
---

This project uses FastAPI + SQLModel + PostgreSQL. Key structural facts:

- `backend/app/crud.py` — single flat CRUD module (not a package). All DB operations live here. Functions are standalone (not class-based), keyword-only args via `*`.
- `backend/app/models.py` — single flat models module. Pattern: `XBase` -> `XCreate`/`XUpdate` -> `X` (table=True) -> `XPublic` -> `XsPublic`.
- `backend/app/api/routes/items.py` — inline query building directly in route handlers using SQLModel `select()`, no CRUD indirection for reads (only `crud.create_item` exists; reads are done inline).
- Pagination: `skip: int = 0, limit: int = 100` query params, applied via `.offset(skip).limit(limit)` on the SQLModel select statement.
- Superuser branching: `read_items` builds two separate `count_statement` + `statement` pairs depending on `current_user.is_superuser`. Both must be updated in tandem for any query change.
- `col()` from sqlmodel used for ordering: `.order_by(col(Item.created_at).desc())`.
- `func` from sqlmodel used for count: `select(func.count()).select_from(Item)`.
- Tests use a real database (session-scoped `db` fixture hitting the actual engine). No mocking.
- `create_random_item(db)` in `tests/utils/item.py` creates a new random user + item each call. `random_lower_string()` returns 32 lowercase ascii chars.
- Test fixtures: `db` (session-scope), `client` (module-scope), `superuser_token_headers` (module-scope), `normal_user_token_headers` (module-scope).
- Item model fields: `title` (str, max 255), `description` (str | None, max 255), `id` (UUID), `owner_id` (UUID FK), `created_at` (datetime).

**Why:** Needed to plan Issue #10 (search filter on GET /items).
**How to apply:** Any new query logic on items must mirror the superuser/non-superuser branching. CRUD functions for reads are not yet extracted — inline query is the established pattern.
