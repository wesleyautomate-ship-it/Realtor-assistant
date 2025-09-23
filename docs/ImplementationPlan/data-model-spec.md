# Data Model Specification (Initial)

Source: Target Tech Spec (extracted) + repository review.

## Core Entities

### User
- id (PK, int)
- email (unique)
- password_hash
- first_name, last_name
- role (enum: client, agent, employee, admin)
- is_active (bool)
- created_at, updated_at

Relations
- has many `UserSession`
- many-to-many `Role` via `user_roles`

### UserSession
- id (PK)
- user_id (FK -> User)
- session_token (unique)
- refresh_token (unique)
- ip_address, user_agent
- expires_at (datetime), is_active (bool)
- created_at, last_used

### Role
- id (PK)
- name (unique)
- description
- is_default (bool)
- created_at, updated_at

Relations
- many-to-many `Permission` via `role_permissions`
- many-to-many `User` via `user_roles`

### Permission
- id (PK)
- name (unique)
- resource (e.g., property, client, task, ai)
- action (read, write, delete, admin)
- description
- created_at

### Property
- id (PK, uuid or int)
- title
- address, location
- property_type (enum)
- bedrooms, bathrooms (int)
- size_sqft (int)
- price (numeric)
- status (enum: active, under_offer, sold, rented)
- created_at, updated_at

Relations
- has many `Media`
- has many `MarketAnalysis`/`CMA`
- links to performance metrics

### Media
- id (PK)
- property_id (FK -> Property)
- url or storage_key
- type (image, doc, video)
- metadata (json)
- uploaded_at

### Client
- id (PK)
- name
- email (unique null-ok), phone (null-ok)
- lead_score (int)
- nurture_status (enum: new, hot, warm, cold)
- last_contacted_at (datetime)
- created_at, updated_at

Relations
- has many `Interaction`
- may reference interested `Property` records (join table optional)

### Interaction
- id (PK)
- client_id (FK -> Client)
- user_id (FK -> User)
- type (email, call, meeting, note)
- notes (text)
- occurred_at (datetime)
- outcome (optional)

### Task
- id (PK)
- owner_user_id (FK -> User)
- title
- description
- status (enum: pending, processing, completed, failed)
- priority (enum: low, normal, high, urgent)
- category (enum)
- due_date (datetime)
- progress (0..100)
- created_at, updated_at

Relations
- optional foreign keys to `Property` and `Client`

### AIRequest
- id (PK)
- user_id (FK -> User)
- source (chat, content, cma, workflow)
- provider (openai)
- request_payload (json)
- response_payload (json)
- status (queued, processing, completed, failed)
- created_at, completed_at

### MarketAnalysis / CMA
- id (PK)
- property_id (FK -> Property)
- suggested_price (numeric)
- market_position (enum: above, at, below)
- confidence (0..1)
- comps_json (json)
- recommendations (text)
- created_at, completed_at

### AnalyticsEvent
- id (PK)
- user_id (FK -> User)
- entity_type (string)
- entity_id (optional)
- metric_type (string)
- value (numeric/string)
- occurred_at (datetime)

## Indices & Constraints
- Unique indices on `User.email`, `UserSession.session_token`, `UserSession.refresh_token`.
- Property: composite indices for common filters (status, price, bedrooms, location).
- Client: indices on `lead_score`, `nurture_status`.
- Task: indices on `owner_user_id`, `status`, `due_date`.

## Migrations Strategy
- Use Alembic to version the schema.
- Seed default roles/permissions via migration or bootstrap script.

## Future Extensions
- Team/Brokerage entities with ownership and sharing rules.
- AuditLog table for security events.
- Materialized views for analytics dashboards.
