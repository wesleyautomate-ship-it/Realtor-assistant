# Agent Alpha-2 Context-Aware Prompts
**Backend Integration Specialist**

---

## **PROMPT A2-A: API DESIGN & DATABASE SETUP (Context-Aware)**

```
AGENT ALPHA-2 - TASK 2A: API DESIGN & DATABASE SETUP

You are Agent Alpha-2, Backend Integration Specialist, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Missing Data Layer entirely (identified as critical gap)
- Gap Analysis Finding: "No CRUD operations, persistence, or caching" 
- Target: Build complete backend API foundation for all S.MPLE categories
- Read docs/PROJECT_CONTEXT_FOR_AGENTS.md for full context

WHAT'S MISSING (FROM ANALYSIS):
❌ Property management API endpoints (for Beta-1's 0% → 100% property system)
❌ Client/CRM API services (for Beta-2's 5% → 100% CRM system) 
❌ Transaction workflow API (for Beta-2's 0% → 100% transaction system)
❌ Marketing campaign APIs (for Beta-3's 40% → 100% marketing enhancement)
❌ Strategy generation APIs (for Beta-4's 5% → 100% strategy system)
❌ Workflow orchestration APIs (for Beta-4's 0% → 100% packages system)

CRITICAL DEPENDENCIES FROM OTHER AGENTS:
- ✅ Check Alpha-1's data models in src/types/ (AGENT_ALPHA1_STATUS.md)
- ✅ Ensure API schemas match Alpha-1's TypeScript interfaces
- Your APIs will enable ALL Beta agents to build their missing features

TASKS:
1. Design REST API endpoints for all S.MPLE categories
2. Create database schema (PostgreSQL/MongoDB) matching Alpha-1's data models
3. Set up API documentation (OpenAPI/Swagger) for Beta agents
4. Implement basic CRUD endpoints for properties, clients, transactions
5. Add authentication and authorization middleware

COORDINATION REQUIREMENTS:
- Review Alpha-1's data models before creating endpoints (avoid mismatches)
- Update AGENT_COORDINATION_LOG.md: "Alpha-2: Core APIs designed and documented"
- Create AGENT_ALPHA2_STATUS.md with endpoint availability status
- Document all endpoints in docs/api-endpoints.md for Beta agents to reference

DELIVERABLES:
- backend/api/properties.js (Property CRUD for Beta-1)
- backend/api/clients.js (Client/CRM CRUD for Beta-2)
- backend/api/transactions.js (Transaction management for Beta-2)
- backend/api/marketing.js (Marketing APIs for Beta-3)
- backend/api/strategy.js (Strategy APIs for Beta-4)
- backend/api/workflows.js (Package orchestration for Beta-4)
- backend/schema/database.sql (Complete database schema)
- docs/api-endpoints.md (API documentation for all Beta agents)

SUCCESS CRITERIA:
- Fix "Missing Data Layer" critical gap from analysis
- Enable all Beta agents to build their 0% → 100% missing systems
- Provide backend foundation for complete S.MPLE framework
- Support real estate workflows: property CRUD, client management, transaction tracking

BEFORE STARTING:
1. Read AGENT_COORDINATION_LOG.md for Alpha-1 completion status
2. Review Alpha-1's TypeScript interfaces in src/types/
3. Ensure database schema matches frontend data models exactly
```

---

## **PROMPT A2-B: WORKFLOW ORCHESTRATION BACKEND (Context-Aware)**

```
AGENT ALPHA-2 - TASK 2B: WORKFLOW ORCHESTRATION BACKEND

You are Agent Alpha-2, continuing backend work for PropertyPro AI workflow automation.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Critical Finding: "No Workflow Engine" identified as major gap
- Target: Enable Beta-4's Packages system (currently 0% complete)
- Packages are core AI automation feature - completely missing
- This backend enables multi-step AI workflow coordination

WHAT'S MISSING FOR WORKFLOW ORCHESTRATION:
❌ Package execution engine (New Listing Package, Lead Nurturing Package)
❌ Multi-step AI coordination backend
❌ Workflow state management and progress tracking
❌ Task automation and scheduling systems
❌ Integration APIs for coordinating all S.MPLE categories

DEPENDENCIES:
- Your completed API foundation from Task 2A
- Alpha-1's workflow data models (src/types/workflow.ts)
- Beta agents will consume these orchestration APIs

TASKS:
1. Create workflow orchestration engine backend
2. Implement package execution system (New Listing, Lead Nurturing packages)
3. Add multi-step AI coordination and state management
4. Build progress tracking and monitoring APIs
5. Create integration layer for coordinating Property + CRM + Marketing + Strategy

COORDINATION:
- This enables Beta-4's complete Packages system (0% → 100%)
- Update AGENT_ALPHA2_STATUS.md: "Workflow orchestration backend complete"
- Document orchestration APIs in docs/workflow-apis.md for Beta-4

DELIVERABLES:
- backend/orchestration/packageEngine.js (Package execution system)
- backend/orchestration/workflowCoordinator.js (Multi-step coordination)
- backend/orchestration/progressTracker.js (Progress monitoring)
- backend/api/packages.js (Package management APIs)
- docs/workflow-apis.md (Documentation for Beta-4)

SUCCESS CRITERIA:
- Fix "No Workflow Engine" critical gap
- Enable Beta-4 to build complete Packages system
- Support AI workflow automation across all S.MPLE categories
- Enable daily workflow automation for realtors
```