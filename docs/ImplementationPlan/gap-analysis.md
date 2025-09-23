# Gap Analysis — Spec vs Current Codebase

Source documents:
- `data/target_tech_spec_f60719e9.txt` (extracted 336-page spec)
- `build_prompt.md`
- Current repo structure and code under `backend/` and `frontend mockup/`

## Executive Summary
- **Overall alignment:** The repository contains many of the right building blocks, but there is architectural drift and duplication. The spec requires a single clean architecture under `backend/app/` with PostgreSQL + Alembic, OpenAI provider, JWT auth/RBAC, and a React Native mobile client. The repo currently mixes a new clean architecture with legacy root-level modules and a web Vite mockup instead of a full React Native app.
- **Top priorities:**
  - Consolidate backend into `backend/app/` and retire overlapping root-level modules.
  - Lock backend port to 8000 (done) and standardize API under `/api/v1`.
  - Implement OpenAI provider formally server-side (remove Gemini fallback, remove hardcoded keys).
  - Establish Alembic migrations for Phase 1 entities and remove production `create_all`.
  - Build out React Native app (`mobile/`) per spec and wire initial flows.

---

## Architecture Alignment
- **Spec:** Clean architecture with Domain, Application/Use Cases, Infrastructure, Presentation.
- **Repo:** `backend/app/` follows the intended structure (`api/`, `domain/`, `infrastructure/`, `core/`), but there are also numerous routers/services at `backend/` root (e.g., `chat_sessions_router.py`, `documents_router.py`, `rag_service.py`) that duplicate or predate the `app/` structure.
- **Gap:** Two parallel architectures cause ambiguity and drift.
- **Action:** Make `backend/app/` the canonical backend. Deprecate and archive root-level duplicates; migrate any unique functionality into `app/` properly.

---

## Backend — Database & Models
- **Spec:** PostgreSQL 15, SQLAlchemy 2.x, Alembic for migrations; entities include `User`, `UserSession`, `Role`, `Permission`, `Property`, `Client`, `Interaction`, `Task`, `AIRequest`, `CMA`, `AnalyticsEvent`, etc. Indices on hot filters.
- **Repo:**
  - `backend/app/core/database.py` uses `StaticPool` which is inappropriate for PostgreSQL (typically for SQLite/in-memory). Port is now aligned to 8000.
  - Models exist in `backend/app/core/models.py` for auth/RBAC; `Base` import path appears inconsistent in some areas.
  - There are migrations folders but also runtime `create_all()` logic.
- **Gaps:**
  - Replace `StaticPool` with proper Postgres pooling.
  - Ensure a single `Base` import and consistent model locations (core vs domain).
  - Remove production `create_all()`. Use Alembic migrations for Phase 1 schema.
- **Actions:**
  - Create Alembic baseline + Phase 1 migration (Users/Sessions/RBAC).
  - Prepare Phase 2 migration (Property/Media/Client/Interaction/Task/AIRequest).
  - Prepare Phase 3 migration (CMA/Nurture/Workflow/Assignment/Approval) and `AnalyticsEvent`.

---

## Backend — API Endpoints
- **Spec Top-10:** `/auth/login`, `/auth/refresh`, `/properties` CRUD, `/clients` CRUD + interactions, `/tasks`, `/ai/generate-content`, `/ai/analyze-property`.
- **Repo:** Numerous routers exist under `backend/app/api/v1/` (e.g., `property_management.py`, `ai_assistant_router.py`, etc.). However, endpoints and contracts must be verified against spec DTOs, and some legacy/duplicate routers exist at repo root.
- **Gaps:**
  - Contract drift: request/response shapes may not match the spec.
  - Versioning and auth consistency across all routers.
- **Actions:**
  - Freeze surface under `/api/v1` and align all routers to the contracts in `docs/ImplementationPlan/api-contracts-v1.md`.
  - Add Pydantic schemas for each route and unify error envelopes.

---

## AI Provider & Services
- **Spec:** OpenAI GPT-4.x (e.g., gpt-4.1/4o) for content/analysis; server-side only; rate limiting & cost control.
- **Repo:** `settings.py` defaults to Gemini and contains a hardcoded fallback Google API key.
- **Gaps:**
  - Wrong default provider and a hardcoded key (security risk).
- **Actions:**
  - Implement `app/infrastructure/ai/openai_provider.py` with env `OPENAI_API_KEY`.
  - Remove Gemini fallback and hardcoded keys. Optionally keep provider interface pluggable but default to OpenAI.

---

## Security & Config
- **Spec:** JWT auth, RBAC, input validation, CORS, rate limiting; audit logs; secure secrets.
- **Repo:** JWT/RBAC scaffolding exists; port updated to 8000; some dev-bypass features and hardcoded values present.
- **Gaps:**
  - Hardcoded Google API key; inconsistent auth across legacy routers; rate limiter not standardized.
- **Actions:**
  - Centralize auth dependencies and rate limits in `app/core/`.
  - Remove any dev bypass in production configurations.
  - Add audit logging events and consistent request logging with correlation IDs.

---

## Frontend — Mobile App
- **Spec:** React Native + TypeScript as primary client; mobile-first UX.
- **Repo:** A Vite web mockup exists (`frontend mockup/`), and a new RN/Expo app has been scaffolded under `mobile/` (Dashboard/Properties/Clients/Content/Tasks/Chat/Analytics).
- **Gaps:**
  - The RN app is new and un-wired to live APIs; no secure token storage yet.
- **Actions:**
  - Implement auth flow in mobile (login + secure token storage).
  - Wire Properties/Clients/Content/Tasks screens to `/api/v1` endpoints.
  - Add basic error/empty states and pagination.

---

## DevOps / Observability
- **Spec:** Health/readiness, metrics, logging, tracing (optional), cost controls.
- **Repo:** Multiple docker-compose files exist; health endpoints not standardized; logs partially implemented.
- **Gaps:**
  - Unified health checks and metrics absent; environment profiles vary.
- **Actions:**
  - Implement `/api/v1/health` (liveness/readiness).
  - Add structured logging and (optional) Prometheus metrics.
  - Standardize docker profiles (dev/staging/prod) and ports.

---

## Prioritized Gap Closure Plan (Milestones)
- **Milestone A — Backend Foundations**
  - Consolidate to `backend/app/` and retire root-level routers.
  - Fix DB engine, add Alembic baseline + Phase 1 migration.
  - Implement `/api/v1/auth/login` and `/api/v1/auth/refresh` with tests.
  - Implement `/api/v1/health`.
- **Milestone B — Core APIs & Mobile Wiring**
  - Implement `/api/v1/properties` and `/api/v1/clients` (+ interactions), `/api/v1/tasks`.
  - Implement OpenAI-backed `/api/v1/ai/generate-content` and `/api/v1/ai/analyze-property`.
  - Wire mobile screens to these endpoints and add secure token storage.
- **Milestone C — Advanced Features**
  - Add Phase 2 migrations (Property/Client/Task/AIRequest) and Phase 3 (CMA/Nurture/Workflow/Assignments/Approvals).
  - Implement CMA and nurturing endpoints; background processing for long tasks.
- **Milestone D — Ops & Analytics**
  - Add AnalyticsEvent, instrumentation, dashboards.
  - Lock security controls: rate limiting, CORS, audit logging, secrets management.

---

## Tracking & Deliverables
- Documentation kept under `docs/ImplementationPlan/`:
  - `phase-01-foundation.md`, `phase-02-core-features.md`, `phase-03-advanced-features.md`, `phase-04-launch-and-ops.md` (to be expanded further with acceptance tests)
  - `data-model-spec.md`, `api-contracts-v1.md`, `analytics-and-kpis.md`, `backend-architecture-refactor.md`, `mobile-app-plan.md`, `gap-analysis.md`

## Next Steps
- Confirm you want me to:
  1) Expand Phase 01 document with full acceptance tests and step-by-step migration/endpoint implementation details, and
  2) Begin implementing Milestone A (migrations + auth endpoints + health) immediately.
