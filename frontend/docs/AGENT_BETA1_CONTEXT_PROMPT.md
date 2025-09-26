# Agent Beta-1 Context-Aware Prompts
**Property & Analytics Specialist**

---

## **PROMPT B1-A: PROPERTY MANAGEMENT SCREENS (Context-Aware)**

```
AGENT BETA-1 - TASK B1-A: PROPERTY MANAGEMENT SCREENS

You are Agent Beta-1, Property & Analytics Specialist, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Property Management is 0% complete (MISSING ENTIRELY)
- Gap Analysis Finding: "No dedicated property management screen exists"
- Target: Build Property Management from 0% → 100% completion
- Read docs/PROJECT_CONTEXT_FOR_AGENTS.md for full context

WHAT'S MISSING (FROM ANALYSIS):
❌ Property CRUD operations (Create, Read, Update, Delete)
❌ MLS integration capability  
❌ Property detail views
❌ Property listing view
❌ Add/edit property functionality

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Grid/list view of property cards with primary photo, title, price, key stats  
- Floating action button (FAB) in bottom-right for adding new property
- Each card shows: bedrooms, bathrooms, square footage
- Quick action icons and property status indicators
- Blue color scheme (#2563eb) for properties and listings

DEPENDENCIES VERIFICATION:
- ✅ Check Alpha-1's propertyStore.ts exists (AGENT_ALPHA1_STATUS.md)
- ✅ Check Alpha-2's property API endpoints documented (AGENT_ALPHA2_STATUS.md) 
- ✅ Review existing components to avoid duplication

TASKS:
1. Create Property List screen (src/screens/PropertiesScreen.tsx) - MISSING
2. Build Property Detail view (src/components/PropertyDetail.tsx) - MISSING
3. Implement Property CRUD operations UI - MISSING  
4. Add property search and filtering - MISSING
5. Create property image management - MISSING

COORDINATION REQUIREMENTS:
- Use propertyStore from Alpha-1's state management
- Integrate with Alpha-2's property API endpoints
- Don't modify components being worked on by Beta-2/Beta-3/Beta-4
- Update AGENT_BETA1_STATUS.md: "Property Management UI complete"
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- src/screens/PropertiesScreen.tsx (DONE)
- src/components/PropertyDetail.tsx (DONE)
- src/components/PropertyForm.tsx (DONE)
- src/components/PropertySearch.tsx (DONE)
- src/components/PropertyCard.tsx (DONE)

SUCCESS CRITERIA:
- Property Management moved from 0% → initial UI completed
- Listing, detail, CRUD form components, and search implemented
- Blue color scheme (#2563eb) applied to key UI elements
- Ready for Beta-3 (Marketing) to leverage property data

BEFORE STARTING:
1. Read AGENT_COORDINATION_LOG.md for latest updates
2. Check Alpha-1 and Alpha-2 status files for dependency completion
3. Review existing screens to understand navigation patterns
```

---

## **PROMPT B1-B: ANALYTICS DASHBOARD ENHANCEMENT (Context-Aware)**

```
AGENT BETA-1 - TASK B1-B: ANALYTICS DASHBOARD ENHANCEMENT

You are Agent Beta-1, continuing Property & Analytics work for PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Analytics is 25% complete (basic KPIs only)
- Critical Missing: CMA Generation (Comparative Market Analysis) - 0% complete
- Target: Analytics from 25% → 100% completion
- Your property data from B1-A will power the analytics

WHAT'S MISSING (FROM ANALYSIS):
❌ CMA (Comparative Market Analysis) generation - CRITICAL P0 ITEM
❌ Market Trends reports (neighborhood-specific analysis)
❌ Performance Review (listing/business analytics) 
❌ Aggressive vs Standard pricing strategies
❌ Comparable property identification (automated comps)

WHAT EXISTS TO ENHANCE:
✅ src/screens/AnalyticsScreen.tsx (40% complete - has basic KPIs)
✅ Basic trending areas list
✅ KPI cards structure

UI/UX REQUIREMENTS:
- Teal color scheme (#0891b2) for analytics and data visualization
- Beautiful charts and graphs using cards to display metrics
- Filter by date range capability
- Export functionality for reports

DEPENDENCIES:
- Your Property data from Task B1-A (propertyStore)
- Alpha-2's analytics APIs  
- Existing AnalyticsScreen.tsx (enhance, don't replace)

TASKS:
1. Enhance existing AnalyticsScreen.tsx with advanced charts
2. Implement CMA generation system (CRITICAL - fills major gap)
3. Add performance metrics and reporting
4. Create market insights with data visualization
5. Add export functionality for reports

COORDINATION:
- Build on existing AnalyticsScreen.tsx (don't overwrite existing work)
- Use analytics data from your propertyStore
- Update AGENT_BETA1_STATUS.md: "Analytics dashboard enhanced"
- Document CMA features in docs/analytics-features.md for other agents

DELIVERABLES:
- Enhanced src/screens/AnalyticsScreen.tsx (25% → 100%)
- src/components/analytics/CMAGenerator.tsx (NEW - fixes critical gap)
- src/components/analytics/PerformanceMetrics.tsx (NEW)
- src/components/analytics/MarketInsights.tsx (enhance existing)
- src/utils/analyticsUtils.ts (NEW)

SUCCESS CRITERIA:
- Fix "CMA Generation missing" critical gap
- Complete Analytics from 25% → 100%
- Enable realtors to generate market analysis reports
- Support daily workflow: AI morning briefing on market conditions
- Provide data for Beta-4's strategy generation

BEFORE STARTING:
1. Ensure B1-A Property Management is complete
2. Review existing AnalyticsScreen.tsx to understand current structure
3. Check Alpha-2's API documentation for analytics endpoints
```

This pattern ensures each agent knows exactly:
1. **What gap they're fixing** from the analysis
2. **The current completion percentage** and target
3. **What exists vs what's missing**  
4. **UI/UX requirements** from the design guide
5. **How their work fits** into the overall S.MPLE framework
6. **Success criteria** based on gap analysis findings