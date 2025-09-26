# Agent Beta-2 Context-Aware Prompts
**CRM & Transactions Specialist**

---

## **PROMPT B2-A: CRM/CLIENT MANAGEMENT INTERFACE (Context-Aware)**

```
AGENT BETA-2 - TASK B2-A: CRM/CLIENT MANAGEMENT INTERFACE

You are Agent Beta-2, CRM & Transactions Specialist, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Client Management is 5% complete (basic ContactManagementView.tsx stub exists)
- Gap Analysis Finding: "No client database integration, No lead scoring system, No communication tracking"
- Target: Build CRM system from 5% → 100% completion
- Read docs/PROJECT_CONTEXT_FOR_AGENTS.md for full context

WHAT'S MISSING (FROM ANALYSIS):
❌ Contact database and management (complete CRM functionality)
❌ Lead scoring system and visualization
❌ Communication history tracking
❌ Client search and filtering capabilities
❌ Quick action icons for call, email, message (from UI/UX requirements)

WHAT EXISTS TO ENHANCE:
✅ src/components/ContactManagementView.tsx (basic stub - enhance, don't replace)
✅ Client action item in navigation (needs full implementation)

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Green color scheme (#059669) for clients and relationship management
- List of clients with name, lead score (visualized with color), last contact date
- Quick action icons for call, email, message
- Client cards should show lead score visualization
- Support daily workflow: lead notification handling with AI-suggested responses

DEPENDENCIES VERIFICATION:
- ✅ Check Alpha-1's clientStore.ts exists and is functional (AGENT_ALPHA1_STATUS.md)
- ✅ Check Alpha-2's client API endpoints are available (AGENT_ALPHA2_STATUS.md)
- ✅ Review existing ContactManagementView.tsx (enhance, don't replace)

TASKS:
1. Enhance existing src/components/ContactManagementView.tsx (don't replace)
2. Create comprehensive Client List screen (src/screens/ClientsScreen.tsx) - NEW
3. Implement lead scoring system and UI visualization - MISSING
4. Add communication tracking and history - MISSING
5. Build client search and filtering - MISSING

COORDINATION REQUIREMENTS:
- Use clientStore from Alpha-1's state management
- Integrate with Alpha-2's client API endpoints
- Don't modify property components (Beta-1's domain)
- Don't modify marketing components (Beta-3's domain)
- Share client data structure with Beta-3 via docs/client-data-structure.md
- Update AGENT_BETA2_STATUS.md: "CRM system complete"
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- Enhanced src/components/ContactManagementView.tsx (5% → 50% improvement)
- src/screens/ClientsScreen.tsx (NEW - main client management screen)
- src/components/ClientDetail.tsx (NEW - individual client details)
- src/components/LeadScoring.tsx (NEW - lead scoring visualization)
- src/components/CommunicationHistory.tsx (NEW - communication tracking)
- docs/client-data-structure.md (for Beta-3 coordination with marketing)

SUCCESS CRITERIA:
- Fix "Client Management 5% complete" gap from analysis
- Implement missing CRM functionality completely
- Follow green color scheme for client-related UI
- Enable Beta-3 (Marketing) to use client data for targeted campaigns
- Support daily workflow: lead notification handling and client communication

BEFORE STARTING:
1. Read AGENT_COORDINATION_LOG.md for latest infrastructure updates
2. Check Alpha-1 and Alpha-2 status files for dependency completion
3. Review existing ContactManagementView.tsx to understand current structure
4. Avoid modifying any property or marketing related components
```

---

## **PROMPT B2-B: TRANSACTION COORDINATION INTERFACE (Context-Aware)**

```
AGENT BETA-2 - TASK B2-B: TRANSACTION COORDINATION INTERFACE

You are Agent Beta-2, continuing CRM & Transactions work for PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Transaction Management is 0% complete (COMPLETE MODULE MISSING)
- Gap Analysis Finding: "No timeline generation, No milestone tracking, No document management"
- Target: Build Transaction system from 0% → 100% completion
- This is a CRITICAL P0 ITEM from gap analysis

WHAT'S MISSING (COMPLETE SYSTEM):
❌ Timeline generation from contract dates - CRITICAL MISSING
❌ Communication templates for milestone emails - MISSING
❌ Workflow automation (task creation and tracking) - MISSING
❌ Document management (transaction document handling) - MISSING
❌ Milestone tracking (inspection, appraisal, closing coordination) - MISSING

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Orange color scheme (#ea580c) for tasks, workflows, and reminders
- Transaction timeline with key dates and milestones
- Progress tracking and status updates
- Integration with client and property data
- Support daily workflow: end-of-day transaction summary

DEPENDENCIES:
- Your completed CRM system from Task B2-A
- Client data integration from your CRM work
- Alpha-2's transaction APIs
- Integration with Beta-1's property data

TASKS:
1. Create Transaction Management screen (src/screens/TransactionsScreen.tsx) - NEW
2. Implement timeline generation from contract dates - CRITICAL MISSING
3. Build milestone tracking system - MISSING
4. Create communication templates for milestones - MISSING
5. Add document management interface - MISSING

COORDINATION REQUIREMENTS:
- Integrate with client data from your completed CRM work (B2-A)
- Transaction data will be used by Beta-4 (Strategy agent) for strategy generation
- Update AGENT_BETA2_STATUS.md: "Transaction system complete"
- Document transaction workflow in docs/transaction-workflow.md (for Beta-4 coordination)
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- src/screens/TransactionsScreen.tsx (NEW - main transaction management)
- src/components/TransactionTimeline.tsx (NEW - timeline generation)
- src/components/MilestoneTracker.tsx (NEW - milestone tracking system)
- src/components/TransactionTemplates.tsx (NEW - communication templates)
- src/components/DocumentManager.tsx (NEW - document management)
- src/utils/transactionUtils.ts (NEW - transaction utilities)
- docs/transaction-workflow.md (for Beta-4 Strategy agent coordination)

SUCCESS CRITERIA:
- Fix "Transaction Management 0% complete" critical gap
- Implement complete transaction coordination system
- Follow orange color scheme for transaction/workflow UI
- Enable Beta-4 to use transaction data for strategy generation
- Support daily workflow: transaction timeline and milestone tracking
- Enable realtors to coordinate inspection, appraisal, closing processes

BEFORE STARTING:
1. Ensure your CRM system from B2-A is complete
2. Check Alpha-2's transaction API availability
3. Plan integration with client data from your CRM work
4. Review Beta-1's property data structure for integration
```