# Phase 04 — Launch & Operations

Scope: Production hardening, monitoring, SLOs, security review, and launch readiness.

## Objectives
- Production-grade deployment (Docker/Compose) with health checks.
- Observability: logging, metrics, tracing, dashboards.
- Security: RBAC review, rate limiting, input validation, secrets management.
- Runbooks, incident response, and post-launch analytics.

## Deployment
- Profiles: `development`, `staging`, `production`.
- Services: API (FastAPI/Uvicorn), Postgres, Redis (optional), Reverse proxy (optional).
- Health endpoints: `/api/v1/health` (liveness/readiness), `/metrics` (if enabled).

## Observability
- Logs: structured JSON logs with request IDs, correlation IDs.
- Metrics: request latency, error rates, throughput, queue length, AI costs.
- Tracing: optional (OpenTelemetry) across API → AI provider calls → DB.

## Security
- JWT auth with refresh; rotation policy.
- RBAC enforcement on critical endpoints.
- Rate limits for costly AI endpoints (per-user/per-minute + burst).
- CORS configuration based on environment.
- Secret management via `.env` (local) and secure store in production.

## Runbooks & Ops
- Incident runbook for API outages, AI provider errors, DB failover.
- Backups/restore process for database (snapshots, PITR if available).
- Cost controls for AI usage (budgets, alerts).

## Acceptance Criteria
- Staging mirrors production topology.
- SLOs defined (e.g., 99.9% uptime, p95 latency < 2s non-AI, < 5s AI).
- Dashboards visible to team; alerts configured for error budgets and costs.
- Launch checklist signed off (security, QA, user acceptance).
