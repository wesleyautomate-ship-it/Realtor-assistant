# Workflow System (Packages) - Agent Beta-4

This document explains the Packages/Workflow orchestration layer added by Agent Beta-4 (B4-B). It coordinates across:

- Beta-1: Property management & analytics (CMA, comps)
- Beta-2: CRM & transactions (clients, lead scoring)
- Beta-3: Marketing & social media (templates, scheduling)
- B4-A: Strategy generation (listing strategy, audience, timeline, negotiation)
- Alpha-2: Workflow orchestration APIs (future integration)

## Architecture Overview

- `frontend/src/utils/packageOrchestration.ts`
  - Defines `PACKAGE_TEMPLATES` (New Listing, Lead Nurture)
  - Exposes helper runners: `runNewListingAnalysis`, `runLeadNurtureAnalysis`
- `frontend/src/services/workflowEngine.ts`
  - Minimal in-memory workflow engine to simulate orchestration
  - Exposes `startRun`, `listRuns`, and run execution lifecycle
- `frontend/src/components/PackagesView.tsx`
  - UI shell for Packages (template launcher, builder, monitor)
- `frontend/src/components/PackageTemplates.tsx`
  - Displays templates and starts a run
- `frontend/src/components/WorkflowMonitor.tsx`
  - Displays execution progress of package runs
- `frontend/src/components/PackageBuilder.tsx`
  - Allows creating custom (mock) multi-step packages (UI scaffold)

## Workflow Templates

1. New Listing Package
   - Step 1: CMA Analysis (Beta-1)
   - Step 2: Listing Strategy (B4-A)
   - Step 3: Marketing Campaign (Beta-3)
   - Step 4: Social Scheduling (Beta-3)

2. Lead Nurturing Package
   - Step 1: Lead Scoring (Beta-2)
   - Step 2: Email Sequence (Beta-3)
   - Step 3: Social Targeting (Beta-3)
   - Step 4: Follow-up Scheduling (Beta-2)

## UI Access

- From dashboard, click `Packages` tile (`frontend/src/constants.tsx`).
- The `PackagesView` will open with:
  - Package Templates (start New Listing or Lead Nurturing)
  - Package Builder (custom workflow scaffold)
  - Workflow Monitor (live progress of runs)

## Alpha-2 Integration Notes

- Current engine is in-memory and simulative.
- Replace `frontend/src/services/workflowEngine.ts` with API calls to Alpha-2 orchestration endpoints when available.
- Expected endpoints (example):
  - `POST /api/v1/orchestration/runs` -> start run
  - `GET /api/v1/orchestration/runs` -> list runs
  - `GET /api/v1/orchestration/runs/{id}` -> run status

## Data Contracts

- Uses `usePropertyStore` and `useClientStore` for data access.
- Strategy outputs are structured (USPs, pricing options, audience segments, timeline, negotiation plays) for orchestration consumption.

## Theming

- Strategy & Packages use teal accents `#0891b2` for visual cohesion.

## Next Steps (Gamma Agents)

- Replace mock engine with Alpha-2 backend orchestration
- Persist custom packages and runs
- Add tasking hooks to Transactions and CRM modules
- Add export/reporting of package outcomes
