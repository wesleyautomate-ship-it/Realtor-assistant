# Database Status Report

Date: 2025-09-23

## Summary
PostgreSQL is provisioned via Docker Compose and used by FastAPI through SQLAlchemy. There are two competing approaches to schema management in the repo: Alembic migrations under `backend/app/alembic/` and an imperative initializer under `backend/app/infrastructure/db/init_database.py` that executes raw SQL and seeds demo data. The baseline migration defines auth/RBAC tables, but feature routers (properties, listing history, confidential tables) expect additional tables that are not yet in migrations.

## Current Artifacts
- **Compose service**: `docker-compose.yml` defines `db` (Postgres 15-alpine) with healthchecks and a volume, and binds `./backend/app/infrastructure/db/migrations` into `/docker-entrypoint-initdb.d` (init scripts run once on first volume creation).
- **SQLAlchemy Base**: `backend/models/__init__.py` exports `Base = declarative_base()`; used by `backend/app/core/models.py` for ORM classes.
- **ORM models**: `backend/app/core/models.py` defines `User`, `UserSession`, `Role`, `Permission`, `AuditLog`, and M2M tables.
- **DB session**: `backend/app/core/database.py` configures engine/session using `DATABASE_URL` and provides `get_db()`, `check_db_connection()`, and bootstrap helpers. Uses `StaticPool` which is atypical for Postgres.
- **Migrations**: `backend/app/alembic/versions/001_phase01_baseline.py` creates users, user_sessions, roles, permissions, role_permissions, user_roles, audit_logs, plus indexes and default seeds.
- **Imperative SQL init**: `backend/app/infrastructure/db/init_database.py` creates additional tables (`properties`, `clients`, `conversations`, `messages`, `conversation_preferences`, `access_audit_log`, `feedback_log`, `response_quality_log`) and inserts samples.

## Gaps / Risks
- **Dual schema sources**: Alembic vs imperative SQL can diverge. Prefer Alembic-only for consistency and migration history.
- **Missing migrations**: Feature routers reference tables not present in Alembic baseline, e.g., `properties`, `listing_history`, and `property_confidential` used by `backend/app/api/v1/property_management.py`.
- **Pooling config**: `StaticPool` in `core/database.py` is suited for in-memory SQLite; for Postgres, use default pooling.
- **Base location**: ORM models import `Base` from `backend/models/__init__.py`, which sits outside `app/` and can be confusing. Co-locate `Base` under `app/core/` or `app/db/` for clarity.
- **Seeding**: Both `core/database.py:init_default_data()` and `init_database.py` seed data. Duplicate responsibilities.

## Prototype Readiness
- Database container is ready and health-checked.
- Minimal auth schema exists via Alembic baseline; but other modules need migrations before end-to-end use.

## Recommended Actions (Next 1–3 days)
- **Unify on Alembic**
  - Migrate SQL from `infrastructure/db/init_database.py` to new Alembic revisions that create `properties`, `clients`, `conversations`, `messages`, `conversation_preferences`, `access_audit_log`, `feedback_log`, `response_quality_log`, and indexes referenced by code.
  - Add migrations for `listing_history` and `property_confidential` tables used by property endpoints.
  - Remove or disable automatic raw-SQL init in production; keep an explicit seed script for dev only.
- **Engine configuration**
  - Replace `StaticPool` with default pool for Postgres in `core/database.py`. Optionally detect SQLite for tests.
- **Consolidate Base**
  - Move `Base = declarative_base()` to `app/core/db.py` or similar and update imports (`from app.core.db import Base`). Update Alembic `env.py` to import correct metadata.
- **Data integrity**
  - Add FK constraints and cascades matching router expectations (e.g., `properties.agent_id -> users.id`).
  - Add not-null and length constraints per business rules.

## Validation Checklist
- Run Alembic upgrade to head and verify all tables exist.
- Start backend and ensure `check_db_connection()` in `health_router` reports `ok`.
- Execute CRUD on properties to confirm schema alignment.

## Effort Estimate
- Porting schema to Alembic + testing: 1–2 days.
- Engine/pool refactor and Base consolidation: 0.5 day.

Overall: 1.5–2.5 days to a consistent, migration-driven database ready for the prototype.
