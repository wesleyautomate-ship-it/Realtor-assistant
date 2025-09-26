# Agent Gamma Context-Aware Prompts
**Integration Agents: AI Integration & Mobile/Design**

---

## **PROMPT G1: CROSS-MODULE AI ENHANCEMENT (Context-Aware)**

```
AGENT GAMMA-1 - TASK G1: CROSS-MODULE AI ENHANCEMENT

You are Agent Gamma-1, AI Integration Coordinator, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: AI Chat is 60% complete (basic chat exists)
- Gap Analysis Finding: "Missing rich formatting, action buttons, voice integration"
- Target: Enhance AI capabilities across ALL completed S.MPLE modules
- This task integrates AI enhancements across the entire completed system

WHAT EXISTS TO ENHANCE:
✅ src/components/ChatView.tsx (basic chat interface - enhance)
✅ Voice recording in MarketingView.tsx (sophisticated - leverage)
✅ AI content generation workflow (build upon)

WHAT'S MISSING FOR AI INTEGRATION:
❌ Rich message formatting in chat interface
❌ Action buttons in AI messages
❌ AI integration across all Beta agent modules (Property, CRM, Marketing, etc.)
❌ Voice integration improvements system-wide
❌ AI prompt templates for each S.MPLE category
❌ AI performance monitoring

CRITICAL PREREQUISITES - ALL MUST BE COMPLETE:
- ✅ Beta-1: Property & Analytics systems (AGENT_BETA1_STATUS.md)
- ✅ Beta-2: CRM & Transaction systems (AGENT_BETA2_STATUS.md)
- ✅ Beta-3: Marketing & Social systems (AGENT_BETA3_STATUS.md)
- ✅ Beta-4: Strategy & Packages systems (AGENT_BETA4_STATUS.md)
- ✅ Review docs/workflow-system.md from Beta-4

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Red color scheme (#dc2626) for AI Assistant and chat interface
- Rich interactions and contextual AI suggestions
- AI suggestions at the right moment (intelligent & contextual)
- Support daily workflows with AI assistance

TASKS:
1. Enhance existing ChatView.tsx with rich interactions (preserve existing, add features)
2. Add AI integration to all completed Beta agent modules
3. Improve voice integration across the entire system
4. Create AI prompt templates for each S.MPLE category
5. Add AI performance monitoring dashboard

AI ENHANCEMENTS FOR EACH MODULE:
- **Property Module (Beta-1):** AI-powered property descriptions, CMA insights
- **CRM Module (Beta-2):** AI client communication suggestions, lead insights
- **Marketing Module (Beta-3):** Enhanced AI content generation (already good)
- **Social Media (Beta-3):** AI post optimization and scheduling suggestions
- **Strategy Module (Beta-4):** AI strategy recommendations and insights
- **Packages (Beta-4):** AI workflow optimization and automation

COORDINATION REQUIREMENTS:
- Enhance existing components, don't replace Beta agents' work
- Add AI capabilities to existing workflows without breaking functionality
- Update AGENT_GAMMA1_STATUS.md: "AI integration complete"
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- Enhanced src/components/ChatView.tsx (60% → 100%)
- src/services/aiCoordinator.ts (NEW - coordinates AI across modules)
- src/utils/aiPromptTemplates.ts (NEW - templates for each S.MPLE category)
- AI enhancements to existing Beta agent components
- src/components/AIMonitor.tsx (NEW - AI performance monitoring)
- src/components/VoiceIntegration.tsx (NEW - enhanced voice features)

SUCCESS CRITERIA:
- Fix "AI Chat 60% complete" gap from analysis
- Add AI capabilities to all S.MPLE modules without breaking existing functionality
- Enable contextual AI suggestions across the entire system
- Support daily workflow with intelligent AI assistance
- Complete AI integration vision for PropertyPro AI

BEFORE STARTING:
1. Verify ALL Beta agents report "complete" status in AGENT_COORDINATION_LOG.md
2. Review each Beta agent's completed modules to understand integration points
3. Test existing AI functionality before adding enhancements
4. Only start when ALL system components are functional
```

---

## **PROMPT G2: MOBILE COMPONENTS & DESIGN SYSTEM (Context-Aware)**

```
AGENT GAMMA-2 - TASK G2: MOBILE COMPONENTS & DESIGN SYSTEM

You are Agent Gamma-2, Mobile & Design System Specialist, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Design system is partial, mobile components at 10%
- Gap Analysis Finding: "Only 2 components have .mobile.tsx variants, no design tokens"
- Target: Complete mobile responsiveness and unified design system
- Transform "Laura AI" branding to "PropertyPro AI" throughout

WHAT EXISTS TO BUILD UPON:
✅ React Native Web architecture working
✅ 2 mobile components: BottomNav.mobile.tsx, CommandCenter.mobile.tsx
✅ Basic responsive design patterns

WHAT'S MISSING (FROM ANALYSIS):
❌ Mobile variants (.mobile.tsx) for all major components
❌ Complete design system in src/theme/
❌ PropertyPro AI branding (currently "Laura AI")
❌ Color-coded system implementation
❌ Design tokens and theme consistency

BRANDING TRANSFORMATION REQUIRED:
- Change "Laura AI" → "PropertyPro AI" throughout the app
- Implement S.MPLE framework branding/messaging
- Apply consistent color-coding system

COLOR-CODED SYSTEM (FROM DESIGN GUIDE):
- Blue (#2563eb): Properties and listings
- Green (#059669): Clients and relationship management
- Purple (#7c3aed): Content generation and marketing materials
- Orange (#ea580c): Tasks, workflows, and reminders
- Red (#dc2626): AI Assistant and chat interface
- Teal (#0891b2): Analytics, reports, and data visualization

CRITICAL PREREQUISITES - ALL MUST BE COMPLETE:
- ✅ ALL Beta agents must be complete (check all status files)
- ✅ All major components must exist before creating mobile variants
- ✅ System functionality must be complete before design polish

TASKS:
1. Create .mobile.tsx variants for all major components created by Beta agents
2. Implement comprehensive design system in src/theme/
3. Transform branding from "Laura AI" to "PropertyPro AI"
4. Ensure responsive design across all screens
5. Implement color-coding system from requirements

MOBILE COMPONENTS TO CREATE:
- All Beta-1 components: PropertyDetail.mobile.tsx, PropertyForm.mobile.tsx, etc.
- All Beta-2 components: ClientDetail.mobile.tsx, TransactionTimeline.mobile.tsx, etc.
- All Beta-3 components: MarketingView.mobile.tsx, SocialMediaView.mobile.tsx, etc.
- All Beta-4 components: StrategyView.mobile.tsx, PackagesView.mobile.tsx, etc.

COORDINATION REQUIREMENTS:
- Don't modify core component logic from Beta agents
- Only add mobile variants and styling enhancements
- Apply color-coding consistently across all modules
- Update AGENT_GAMMA2_STATUS.md: "Mobile & design complete"
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- Mobile variants (.mobile.tsx) for all major components
- src/theme/ directory with complete design system:
  - src/theme/colors.ts (color-coded system)
  - src/theme/typography.ts (typography scale)
  - src/theme/spacing.ts (spacing system)
  - src/theme/components.ts (component themes)
- Brand consistency updates (PropertyPro AI throughout)
- Responsive design implementation across all screens

SUCCESS CRITERIA:
- Fix "Mobile components 10% complete" gap
- Complete design system with proper color-coding
- Transform branding to PropertyPro AI consistently
- Enable thumb-friendly mobile operation (design guide requirement)
- Support mobile-first daily workflows for realtors
- Complete the professional UI/UX vision

BEFORE STARTING:
1. Wait for ALL component development to complete first
2. Review all Beta agent deliverables to understand components needing mobile variants
3. Create comprehensive list of components requiring .mobile.tsx variants
4. Plan color-coding application across all modules
5. Only start when ALL Beta agents report completion
```