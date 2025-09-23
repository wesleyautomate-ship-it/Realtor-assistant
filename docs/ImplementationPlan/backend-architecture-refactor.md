# Backend Architecture Refactor Plan

Source: Target Tech Spec + current repository audit.

## Goals
- Consolidate to a single clean architecture under `backend/app/`.
- Align with PostgreSQL + Alembic migrations; remove runtime `create_all()` from production code paths.
- Implement OpenAI provider as the default AI service.
- Normalize configuration, ports, CORS, and security.

## Consolidation
- Canonical app root: `backend/app/`
  - Keep: `app/api/v1/`, `app/domain/`, `app/infrastructure/`, `app/core/`
  - Deprecate/retire overlapping routers and services in `backend/` (root-level duplicates)
  - Ensure `app/main.py` includes only the v1 router set and middleware.

## Configuration & Security
- `app/core/settings.py`
  - Default `PORT=8000` (done)
  - Remove any hard-coded API keys; use `.env` for `OPENAI_API_KEY`
  - CORS: development allows `http://localhost:*`; staging/production restricted
- Secrets
  - `.env.example` updated with required keys
- Rate limiting
  - Add simple in-memory limiter for dev; Redis option for staging/prod

## Database
- PostgreSQL connection pool (no `StaticPool`)
- Alembic migrations for:
  - Phase 01: Auth + RBAC (`User`, `UserSession`, `Role`, `Permission`, M:N tables)
  - Phase 02: `Property`, `Media`, `Client`, `Interaction`, `Task`, `AIRequest`
  - Phase 03: `CMA`, `NurtureSequence`, `NurtureRun`, `WorkflowEvent`, `Assignment`, `Approval`
  - Analytics: `AnalyticsEvent`
- Seeding script for default roles/permissions and an admin user (dev only)

## API Surface (v1)
- Mount under `/api/v1`
- Auth: `/auth/login`, `/auth/refresh`
- Properties: `/properties`, `/properties/{id}`, `/properties/{id}/images`
- Clients: `/clients`, `/clients/{id}`, `/clients/{id}/interactions`
- Tasks: `/tasks`, `/tasks/{id}`
- AI: `/ai/generate-content`, `/ai/analyze-property` (OpenAI)
- Analytics: event ingest internal endpoint (optional)

## Middleware & Observability
- Request/response logging with correlation IDs
- Error handler returning standard error envelope
- Metrics counters/timers (optional Prometheus)

## OpenAI Provider Implementation
- `app/infrastructure/ai/openai_provider.py`
  - `generate_content(prompt, content_type, tone)`
  - `analyze_property(description, details)`
- Service layer (`app/domain/ai/ai_service.py`) orchestrates calls and normalization
- Configurable model defaults (e.g., `gpt-4o` or `gpt-4.1`)

## Background Processing
- For long-running AI tasks (e.g., CMA):
  - Start with FastAPI background tasks
  - Optionally introduce Celery/Redis in Phase 03

## Migration Plan
- Step 1: Lock router set to `/api/v1` in `app/main.py`
- Step 2: Add Alembic with baseline migration for Phase 01
- Step 3: Implement Auth endpoints + tests
- Step 4: Add Phase 02 schema and endpoints incrementally
- Step 5: Integrate OpenAI provider and wire AI endpoints

## Acceptance Criteria
- Running `alembic upgrade head` on a fresh DB bootstraps the schema
- `/api/v1/auth/login` and protected routes pass integration tests
- AI endpoints return content with OpenAI using server-side key (no client exposure)
