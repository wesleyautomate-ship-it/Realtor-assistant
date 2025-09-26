Workflow Orchestration APIs (Beta-4)
====================================

Base Prefix: `/api/v1/orchestration`

Task Endpoints
--------------
- POST `/tasks` — submit AI task
- GET `/tasks/{task_id}` — get task status
- DELETE `/tasks/{task_id}` — cancel task (queued/processing)

Package Endpoints
-----------------
- GET `/packages` — list available packages (listing, nurturing, onboarding)
- POST `/packages/execute` — execute package with context
- GET `/packages/status/{execution_id}` — check execution status
- POST `/packages/custom` — create custom package (admin/agent)

Quick Start
-----------
- POST `/quick/new-listing` — runs CMA → Strategy → Marketing → Approval → Launch
- POST `/quick/lead-nurturing` — runs Qualification → Email → Recommendations → Follow-up

Data Model (Orchestration Tables)
---------------------------------
- `ai_tasks`: status/progress for individual tasks
- `package_executions`: overall execution tracking
- `package_steps`: step-level progress and outputs

Integration
-----------
- Coordinates existing routers: Properties, Clients, Marketing, CMA, Social
- Consumed by Beta-4 Packages UI for monitoring and control


