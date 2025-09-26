# Client Data Structure

Shared client schema for CRM (Beta-2) and Marketing (Beta-3).

Fields:
- id: string
- name: string
- email?: string
- phone?: string
- leadScore?: number (0-100)
- status: 'new' | 'contacted' | 'qualified' | 'nurturing' | 'converted' | 'archived'
- lastContactedAt?: ISO string
- notes?: string

CommunicationLog:
- id: string
- clientId: string
- type: 'call' | 'email' | 'sms' | 'meeting'
- content?: string
- at: ISO string

Store selectors and hooks are exported from `src/store/index.ts` as `useClientStore`, `selectClients`, `selectClientById`.

API endpoints (Alpha-2):
- GET `/api/v1/clients`
- POST `/api/v1/clients`
- POST `/api/v1/clients/{id}` with `{ _method: 'PATCH', ...updates }`
- POST `/api/v1/clients/communications`

Color theme for client UI: emerald `#059669`.


