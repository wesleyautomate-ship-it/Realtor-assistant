# Phase 02 — Core Features

Scope: Deliver the platform’s main business capabilities across Properties, Clients, Content, Tasks, and AI.

## Objectives
- Property management end-to-end (CRUD, images, performance metrics).
- Client management with lead scoring and interaction history.
- AI content generation endpoints (OpenAI-backed) for descriptions/social/email/brochures.
- Task engine for smart creation and prioritization; reminders.

## Data Model Additions
- `Property(id, title, address, location, type, bedrooms, bathrooms, size_sqft, price, status, created_at, updated_at)`
- `Media(id, property_id, url, type, meta, uploaded_at)`
- `Client(id, name, email, phone, lead_score, nurture_status, last_contacted_at, created_at, updated_at)`
- `Interaction(id, client_id, user_id, type, notes, occurred_at, outcome)`
- `Task(id, owner_user_id, title, description, status, priority, category, due_date, progress, created_at, updated_at)`
- `AIRequest(id, user_id, source, provider, request_payload, response_payload, status, created_at, completed_at)`

## APIs (v1)
- Properties
  - `GET /api/v1/properties`
  - `POST /api/v1/properties`
  - `GET /api/v1/properties/{id}`
  - `PATCH /api/v1/properties/{id}`
  - `POST /api/v1/properties/{id}/images` (multipart)
- Clients
  - `GET /api/v1/clients`
  - `POST /api/v1/clients`
  - `GET /api/v1/clients/{id}`
  - `PATCH /api/v1/clients/{id}`
  - `POST /api/v1/clients/{id}/interactions`
- AI Content/Analysis (OpenAI)
  - `POST /api/v1/ai/generate-content`
  - `POST /api/v1/ai/analyze-property`
- Tasks
  - `GET /api/v1/tasks`
  - `POST /api/v1/tasks`
  - `PATCH /api/v1/tasks/{id}`

## Mobile Deliverables
- Properties list/detail screens; create property flow.
- Clients list/detail screens; add interaction; lead status update.
- Content screen to request and display generated outputs; copy/share.
- Tasks screen to view/complete tasks; reminders UI.

## Acceptance Criteria
- Endpoints secured via JWT; RBAC applied where relevant.
- Images stored and retrievable; metadata captured.
- AI responses returned within SLA or queued with status polling.
- Tasks auto-created from significant events (e.g., new property or client).

## Risks & Mitigations
- AI cost/latency: add queuing, caching for repeated prompts, and sensible token limits.
- PII protection: input validation + redaction where appropriate.
