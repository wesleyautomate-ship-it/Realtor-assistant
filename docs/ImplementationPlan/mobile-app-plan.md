# Mobile App Implementation Plan (React Native + Expo)

## Goals
- Deliver a mobile-first experience aligned with the PDF spec and `build_prompt.md`.
- Implement the six core areas with a clean navigation structure and type-safe services.

## Stack
- React Native 0.74 + Expo SDK ~51
- TypeScript 5.x
- Navigation: `@react-navigation/native` + native-stack

## Screens & Navigation
- Dashboard
- Properties (List/Detail/Create)
- Clients (List/Detail/Create, Interactions)
- Content (AI requests)
- Tasks (List/Detail/Update)
- Chat (AI Assistant)
- Analytics (Overview charts, KPIs)

## Service Layer
- `src/services/api.ts` — base HTTP (fetch)
- `src/services/ai/index.ts` — calls OpenAI-backed backend endpoints
- `src/config.ts` — reads `API_BASE_URL` and provider settings from `app.json`

## Data Types (client-side)
- Mirror server DTOs from `docs/ImplementationPlan/api-contracts-v1.md`

## Flows (Phase-by-Phase)
- Phase 01
  - Login screen → store tokens securely (Expo SecureStore)
  - Health check + basic routing guard
- Phase 02
  - Properties: list/detail/create; image upload
  - Clients: list/detail/create; log interaction
  - Content: submit prompt → show AI results with copy/share
  - Tasks: list/update status
- Phase 03
  - CMA flow with progress; nurture sequences
  - Review/approve cards; assignments
- Phase 04
  - Analytics charts; error/reporting screens; settings

## QA & Performance
- Unit tests for hooks/services
- E2E flows with Detox (optional future)
- Performance: avoid unnecessary re-renders; paginate lists; cache responses

## Acceptance Criteria
- App compiles and runs in Expo (iOS/Android/Web)
- Screens can perform primary operations against live API
- Error and empty states are handled gracefully
