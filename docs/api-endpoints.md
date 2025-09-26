PropertyPro AI API Endpoints (Alpha-2)
======================================

Base URL: `/api`

Properties
----------
- GET `/api/properties/` — list properties
- POST `/api/properties/` — create property
- GET `/api/properties/search` — search properties
- GET `/api/properties/{id}` — get property details
- PUT `/api/properties/{id}` — update property
- PUT `/api/properties/{id}/status` — update listing status
- POST `/api/properties/{id}/ai-pricing` — AI pricing recommendation

Clients (CRM)
-------------
- GET `/api/v1/clients/` — list clients
- GET `/api/v1/clients/{id}` — get client
- POST `/api/v1/clients/` — create client (agent/admin)
- PUT `/api/v1/clients/{id}` — update client (agent/admin)
- DELETE `/api/v1/clients/{id}` — delete client (agent/admin)

Transactions
------------
- GET `/api/v1/transactions/` — list transactions
- GET `/api/v1/transactions/{id}` — get transaction
- POST `/api/v1/transactions/` — create transaction (agent/admin)
- PUT `/api/v1/transactions/{id}` — update transaction (agent/admin)
- POST `/api/v1/transactions/{id}/status` — change status (agent/admin)
- DELETE `/api/v1/transactions/{id}` — delete transaction (agent/admin)

Marketing (AURA)
----------------
- Prefix: `/api/v1/marketing` — campaigns, templates, packages

Workflows (AURA)
----------------
- Prefix: `/api/v1/workflows` — list/execute packages, status

CMA & Social (AURA)
-------------------
- CMA: `/api/v1/cma/*`
- Social: `/api/v1/social/*`

Auth & Health
-------------
- `/api/v1/auth/*`, `/api/v1/health`


