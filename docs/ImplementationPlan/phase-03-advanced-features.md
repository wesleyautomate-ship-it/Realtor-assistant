# Phase 03 — Advanced Features

Scope: Elevate intelligence, automation, and collaboration.

## Objectives
- Comparative Market Analysis (CMA) and Market Intelligence.
- Automated follow-ups and nurturing sequences with configurable playbooks.
- Workflow automation (event-driven) and queue-based background processing.
- Collaboration features: assignments, mentions, review/approve flows.

## Data Model Additions
- `CMA(id, property_id, suggested_price, market_position, confidence, comps_json, recommendations, created_at, completed_at)`
- `NurtureSequence(id, name, description, triggers, steps_json, created_by, created_at)`
- `NurtureRun(id, sequence_id, client_id, status, next_action_at, last_action_at, created_at, updated_at)`
- `WorkflowEvent(id, event_type, entity_type, entity_id, payload_json, created_at)`
- `Assignment(id, entity_type, entity_id, assignee_user_id, status, created_at, updated_at)`
- `Approval(id, entity_type, entity_id, requested_by, approved_by, status, notes, created_at, updated_at)`

## APIs (v1)
- CMA
  - `POST /api/v1/analytics/cma` — initiate CMA
  - `GET /api/v1/analytics/cma/{id}` — status + results
- Nurturing
  - `POST /api/v1/nurturing/sequences`
  - `GET /api/v1/nurturing/sequences`
  - `POST /api/v1/nurturing/runs`
  - `GET /api/v1/nurturing/runs/{id}`
- Workflow & Collaboration
  - `POST /api/v1/workflows/events` (internal use)
  - `POST /api/v1/assignments`
  - `POST /api/v1/approvals`

## Mobile Deliverables
- CMA screen with progress and results (pricing suggestions, comps summary).
- Nurturing configuration UI and run tracking.
- Review/approval actions embedded in request cards.

## Non-Functional
- Background jobs for long-running AI/market calls.
- Idempotency and retry policies (timeouts, exponential backoff, circuit breakers).

## Acceptance Criteria
- CMA completes with suggested price and recommendations, or returns queued status with polling.
- Nurture runs proceed through steps automatically and log interactions.
- Approvals/assignments update state consistently and reflect in UI.
