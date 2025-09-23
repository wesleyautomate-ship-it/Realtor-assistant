# Setup & Infrastructure Status Report

Date: 2025-09-23

## Summary
The repository provides a robust local/dev and containerized setup: Docker Compose orchestrates Postgres, Redis, ChromaDB, FastAPI API, Celery worker/beat, and an optional Nginx and frontend (mockup). A comprehensive `Makefile` offers common workflows. Environment configuration is centralized via `env.example` and referenced in Compose.

## Current Artifacts
- **Compose files**: `docker-compose.yml` (primary), plus secure/monitoring/staging variants.
- **Services**: `db` (Postgres 15), `redis` (7), `chromadb`, `api` (backend Dockerfile), `worker`, `scheduler`, `frontend` (mockup via Vite+Nginx), optional `nginx`, and `e2e` Playwright.
- **Healthchecks**: Present for `db`, `redis`, `chromadb`, `api`, `worker`.
- **Env**: `env.example` is complete with DB, Redis, Chroma, JWT, OpenAI, SMTP, Twilio, Stripe, Sentry, Prometheus.
- **Makefile**: Rich command set for build/up/down, logs, tests, lint/format, migrations, health, backup/restore, and dev helpers.
- **Monitoring**: `monitoring/` directory includes Prometheus/Grafana configs and Python helpers.

## Gaps / Risks
- **Security**: `backend/app/core/settings.py` contains a hardcoded fallback Google API key; remove and mandate env variable.
- **Schema init path**: Compose mounts `./backend/app/infrastructure/db/migrations` into `/docker-entrypoint-initdb.d`, but Alembic migrations are located at `backend/app/alembic/`. Ensure the intended init scripts are correct and that we don't have two schema authorities (Raw SQL vs Alembic).
- **CORS/Origins**: `ALLOWED_ORIGINS` uses broad patterns for dev (ngrok wildcards). Confirm for production profiles.
- **Ports**: Defaults are open to localhost; for production, deploy behind Nginx with SSL and restrict direct API port if needed.
- **E2E**: Playwright config references `frontend mockup/`. Confirm this folder builds and routes API calls properly.

## Prototype Readiness
- Running `docker-compose up -d` should bring up core services and the API at `http://localhost:8000` and frontend mockup at `http://localhost:3000`.
- Health checks help confirm container readiness.

## Recommended Actions (Next 1–2 days)
- **Secrets hygiene**
  - Remove fallback keys from source code. Validate env on startup using `validate_settings()`.
- **Migrations alignment**
  - Decide: use Alembic as the authoritative migration tool. Stop mounting raw SQL init scripts, or keep them only for the initial baseline that delegates to Alembic.
- **Developer docs**
  - Add a short README section for "Start the prototype" with steps: copy `.env`, `docker-compose up -d`, run Alembic upgrade, seed admin.
- **CI**
  - Add a basic CI workflow to lint and run a minimal backend test suite.
- **Container polish**
  - Ensure API container `healthcheck` hits `/health` reliably; confirm Uvicorn workers and graceful shutdowns.

## Validation Checklist
- `make up` brings up all services without errors.
- `make health` shows API healthy and DB ready.
- Alembic migration to head succeeds inside `api` container.
- Frontend mockup serves via Nginx and can hit API route (CORS ok).

## Effort Estimate
- 0.5–1 day to tighten security and migration path and update docs.
