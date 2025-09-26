# Agent Beta-3 Context-Aware Prompts
**Marketing & Social Media Specialist**

---

## **PROMPT B3-A: MARKETING CAMPAIGN ENHANCEMENT (Context-Aware)**

```
AGENT BETA-3 - TASK B3-A: MARKETING CAMPAIGN ENHANCEMENT

You are Agent Beta-3, Marketing & Social Media Specialist, part of an 8-agent team building PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Marketing is 40% complete (good foundation exists)
- Gap Analysis Finding: "Sophisticated MarketingView.tsx (710 lines) with voice recording and AI generation"
- Target: Enhance Marketing from 40% → 100% completion
- Read docs/PROJECT_CONTEXT_FOR_AGENTS.md for full context

WHAT EXISTS TO PRESERVE & ENHANCE:
✅ src/components/MarketingView.tsx (710 lines of sophisticated code - PRESERVE)
✅ Voice recording with audio level monitoring and waveform visualization
✅ AI content generation workflow (step-by-step process)
✅ Property selection UI for marketing campaigns
✅ Text and voice input for AI instructions

WHAT'S MISSING (FROM ANALYSIS):
❌ Postcard mailer templates and design generation
❌ Multi-channel campaign creation (email, social, print coordination)
❌ Email blast generation and automation
❌ Print-ready design export functionality
❌ Integration with property data for auto-population (from Beta-1)

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Purple color scheme (#7c3aed) for content generation and marketing materials
- Template gallery with branded designs
- Multi-platform campaign coordination
- Support daily workflow: one-tap social media posting for new listings

DEPENDENCIES CHECK:
- ✅ Review existing MarketingView.tsx carefully (enhance, don't replace)
- ✅ Check Beta-1's property data availability (for auto-population)
- ✅ Verify Alpha-2's marketing APIs are documented

TASKS:
1. ENHANCE existing MarketingView.tsx with postcard template system (preserve existing 710 lines)
2. Add multi-channel campaign creation (email + social + print coordination)
3. Implement email blast generation and templates 
4. Create print-ready design export functionality
5. Add campaign performance tracking and analytics

CRITICAL PRESERVATION REQUIREMENTS:
- DO NOT replace or rewrite existing MarketingView.tsx
- PRESERVE all existing voice recording functionality
- PRESERVE existing AI generation workflow
- PRESERVE existing property selection UI
- BUILD ON TOP of existing sophisticated features

COORDINATION REQUIREMENTS:
- Use property data from Beta-1's propertyStore for auto-populated campaigns
- Don't modify social media components yet (next task B3-B)
- Update AGENT_BETA3_STATUS.md: "Marketing campaigns enhanced"
- Update AGENT_COORDINATION_LOG.md with completion

DELIVERABLES:
- Enhanced src/components/MarketingView.tsx (preserve existing + add missing features)
- src/components/PostcardTemplates.tsx (NEW - postcard mailer system)
- src/components/EmailCampaigns.tsx (NEW - email blast generation)
- src/components/MarketingTemplates.tsx (NEW - template gallery)
- src/utils/designExport.ts (NEW - print-ready export)
- src/components/CampaignAnalytics.tsx (NEW - performance tracking)

SUCCESS CRITERIA:
- Fix Marketing gaps while preserving existing 40% functionality
- Complete Marketing from 40% → 100%
- Enable multi-channel campaigns (property → email + social + print)
- Support daily workflow: automated marketing for new listings
- Maintain existing voice recording and AI generation capabilities

BEFORE STARTING:
1. Read and understand existing MarketingView.tsx thoroughly (710 lines)
2. Check Beta-1's property data structure for integration
3. Plan enhancements that BUILD ON existing code, don't replace it
4. Verify you can access property data for auto-population
```

---

## **PROMPT B3-B: SOCIAL MEDIA PLATFORM INTEGRATION (Context-Aware)**

```
AGENT BETA-3 - TASK B3-B: SOCIAL MEDIA PLATFORM INTEGRATION

You are Agent Beta-3, continuing Marketing & Social Media work for PropertyPro AI.

PROJECT CONTEXT FROM GAP ANALYSIS:
- Current Status: Social Media is 20% complete (basic SocialMediaView.tsx structure exists)
- Gap Analysis Finding: "Basic social media view structure exists but no real functionality"
- Target: Build Social Media from 20% → 100% completion
- This builds on your enhanced Marketing system from B3-A

WHAT EXISTS TO ENHANCE:
✅ src/components/SocialMediaView.tsx (basic structure - build it out fully)
✅ Social media action item in navigation

WHAT'S MISSING (FROM ANALYSIS):
❌ Category-based posts ("Just Listed", "Open House", "In-Contract", "Just Sold" templates)
❌ Template gallery with branded design selection
❌ Platform integration (Facebook, Instagram, LinkedIn APIs)
❌ Automated posting and scheduling functionality
❌ Property photo integration (auto property image insertion)

UI/UX REQUIREMENTS (FROM DESIGN GUIDE):
- Purple color scheme (#7c3aed) for social media content generation
- Template-based generation with branded templates
- Multi-platform campaigns (Instagram, Facebook, LinkedIn)
- Support daily workflow: one-tap social media posting for new listings

DEPENDENCIES:
- Your enhanced marketing system from Task B3-A
- Property data from Beta-1 for auto-populated posts
- Client data structure from Beta-2 (check docs/client-data-structure.md)

TASKS:
1. Transform src/components/SocialMediaView.tsx into full platform
2. Implement Facebook, Instagram, LinkedIn API integration
3. Create template gallery with branded designs for real estate categories
4. Add automated posting and scheduling functionality
5. Build multi-platform campaign coordination with your marketing system

SOCIAL MEDIA TEMPLATE CATEGORIES (MUST IMPLEMENT):
- "Just Listed" posts with property details and photos
- "Open House" announcements with date/time
- "In-Contract" celebration posts
- "Just Sold" success posts with market insights
- Custom campaign posts coordinated with marketing

COORDINATION REQUIREMENTS:
- Use marketing content from your enhanced system (B3-A)
- Integrate with Beta-1's property data for auto-populated posts
- Share social content templates with Beta-4 for strategy packages
- Update AGENT_BETA3_STATUS.md: "Social media integration complete"
- Create docs/social-templates.md for Beta-4 coordination

DELIVERABLES:
- Comprehensive src/components/SocialMediaView.tsx (20% → 100%)
- src/components/SocialTemplates.tsx (NEW - branded template gallery)
- src/components/PostScheduler.tsx (NEW - automated posting)
- src/components/PlatformConnections.tsx (NEW - API integrations)
- src/components/SocialCampaigns.tsx (NEW - multi-platform coordination)
- src/services/socialMediaApi.ts (NEW - social platform APIs)
- docs/social-templates.md (for Beta-4 coordination)

SUCCESS CRITERIA:
- Fix "Social Media 20% complete" gap from analysis
- Implement complete social media platform with automation
- Enable multi-platform posting (Facebook, Instagram, LinkedIn)
- Support daily workflow: one-tap posting for property milestones
- Integrate with property and marketing data for automated content
- Provide social templates for Beta-4's strategy packages

BEFORE STARTING:
1. Ensure your Marketing enhancement from B3-A is complete
2. Check Beta-2's client data structure for targeted campaigns
3. Review existing SocialMediaView.tsx structure
4. Plan integration with your enhanced marketing campaigns
```