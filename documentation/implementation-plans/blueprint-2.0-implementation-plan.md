# Blueprint 2.0: The Proactive AI Copilot - Implementation Plan

## Overview

This implementation plan outlines the development roadmap for transforming the RAG web app into a proactive AI copilot with two key focus areas:

1. **Web-Based Content Delivery**: Shifting from static PDF generation to live, shareable web links for content like CMAs, complete with previews in the chat.

2. **Proactive Lead Nurturing**: Evolving the CRM from a reactive command-taker to a proactive assistant that suggests follow-ups and helps agents with communication.

## Phase 1: Database Schema Updates

### 1.1 Generated Documents Table Enhancement

**Add new columns to `generated_documents` table:**
- `content_html` (TEXT) - Store the generated HTML content
- `preview_summary` (TEXT) - Store the 1-2 sentence summary for preview
- `result_url` (VARCHAR) - Store the shareable URL
- `document_type` (VARCHAR) - Distinguish between CMA, brochure, etc.

**Deprecate/repurpose:** `file_path` column (can be kept for backward compatibility)

### 1.2 Leads Table Enhancement

**Add new columns to `leads` table:**
- `last_contacted_at` (TIMESTAMP)
- `next_follow_up_at` (TIMESTAMP)
- `nurture_status` (VARCHAR) - Values: 'Hot', 'Warm', 'Cold', 'Needs Follow-up'
- `assigned_agent_id` (UUID) - Link to user who owns this lead

### 1.3 Lead History Table Creation

**Create new `lead_history` table:**
- `id` (UUID, Primary Key)
- `lead_id` (UUID, Foreign Key to leads)
- `agent_id` (UUID, Foreign Key to users)
- `interaction_type` (VARCHAR) - 'call', 'email', 'meeting', 'note'
- `content` (TEXT) - Details of the interaction
- `created_at` (TIMESTAMP)
- `scheduled_for` (TIMESTAMP, nullable) - For future scheduled interactions

### 1.4 Tasks/Notifications Table Enhancement

**Add new columns to existing tasks table or create new `notifications` table:**
- `notification_type` (VARCHAR) - 'follow_up', 'nurture_suggestion', 'scheduled_task'
- `related_lead_id` (UUID, nullable)
- `related_document_id` (UUID, nullable)
- `priority` (VARCHAR) - 'high', 'medium', 'low'

## Phase 2: Backend Implementation

### 2.1 Document Generation System Overhaul

**Modify `ai_manager.py`:**
- Update `generate_cma_document` to create HTML instead of PDF
- Create HTML templates for different document types (CMA, brochure, etc.)
- Implement preview summary generation
- Store HTML content and summary in database

### 2.2 New Document Router

**Create `documents_router.py`:**
- `GET /documents/view/{document_id}` - Serve HTML content
- `GET /documents/{document_id}/preview` - Get preview data
- `POST /documents/generate` - Initiate document generation
- Implement permission checking for document access

### 2.3 Enhanced Action Engine

**Extend `action_engine.py`:**
- `get_follow_up_context(lead_id)` - Retrieve lead history and profile
- `create_nurture_suggestion(lead_id)` - Generate follow-up suggestions
- `schedule_follow_up(lead_id, date)` - Schedule future interactions

### 2.4 Proactive Nurturing System

**Enhance `scheduler.py`:**
- Daily follow-up job (7 AM) - Check for scheduled follow-ups
- Nurture identification job (8 AM) - Find leads needing attention
- Create notification tasks for agents
- Update lead nurture status automatically

### 2.5 New API Endpoints

**Create `nurturing_router.py`:**
- `GET /users/me/agenda` - Get today's tasks and suggestions
- `GET /leads/{lead_id}/history` - Get lead interaction history
- `POST /leads/{lead_id}/interaction` - Log new interaction
- `PUT /leads/{lead_id}/follow-up` - Schedule follow-up
- `GET /notifications` - Get user notifications
- `PUT /notifications/{id}/read` - Mark notification as read

## Phase 3: Frontend Implementation

### 3.1 Enhanced Chat Interface

**Update `Chat.jsx`:**
- Add `ContentPreviewCard` component for document previews
- Implement polling for async task completion
- Display shareable links with preview summaries
- Add lead context panel when typing client names

### 3.2 New Dashboard Components

**Create `TodaysAgenda.jsx`:**
- Display scheduled tasks and follow-ups
- Show nurture suggestions
- Quick action buttons for common tasks

**Create `NotificationsPanel.jsx`:**
- Bell icon in header
- Dropdown with unread notifications
- Mark as read functionality

### 3.3 Lead Management Interface

**Create `LeadContext.jsx`:**
- Display lead status and last contact
- Quick access to interaction history
- Follow-up suggestion display

### 3.4 Document Preview Components

**Create `ContentPreviewCard.jsx`:**
- Display document preview summary
- "View Full Report" button
- Document type indicator

## Phase 4: AI Integration Enhancements

### 4.1 Enhanced Prompt Engineering

**Update system prompts in `rag_service.py`:**
- Add context for lead nurturing suggestions
- Include document generation templates
- Enhance follow-up message generation

### 4.2 Context-Aware Responses

**Modify chat processing:**
- Detect when user mentions a lead name
- Provide relevant lead context automatically
- Suggest follow-up actions based on lead status

## Phase 5: Testing and Validation

### 5.1 Database Migration Scripts
- Create migration scripts for all schema changes
- Test data migration from existing structure
- Validate foreign key relationships

### 5.2 Integration Testing
- Test document generation workflow end-to-end
- Validate nurturing system triggers
- Test notification delivery

### 5.3 User Experience Testing
- Test document preview functionality
- Validate proactive suggestions
- Test lead context integration

## Phase 6: Deployment and Monitoring

### 6.1 Environment Configuration
- Update Docker Compose for new services
- Configure scheduler timezone settings
- Set up monitoring for background jobs

### 6.2 Performance Optimization
- Implement caching for frequently accessed lead data
- Optimize database queries for lead history
- Add indexing for new columns

## Implementation Priority Order

### High Priority (Week 1-2)
- Database schema updates
- Basic document generation with HTML
- Document viewing endpoints

### Medium Priority (Week 3-4)
- Lead history tracking
- Basic nurturing system
- Frontend document previews

### Lower Priority (Week 5-6)
- Advanced proactive features
- Enhanced AI integration
- Performance optimization

## Risk Mitigation

### Backward Compatibility
- Keep existing PDF generation as fallback
- Maintain existing API endpoints during transition

### Gradual Rollout
- Implement features incrementally
- Use feature flags for new functionality
- Monitor system performance during rollout

### Data Safety
- Create backups before schema changes
- Test migrations in staging environment
- Implement rollback procedures

### Monitoring and Alerting
- Add logging for all new background processes
- Monitor database performance with new queries
- Set up alerts for failed background jobs

## Success Metrics

### User Engagement
- Document generation completion rate
- Time spent on lead nurturing features
- User adoption of proactive suggestions

### System Performance
- Document generation response time
- Background job completion rates
- Database query performance

### Business Impact
- Lead follow-up completion rates
- Time saved on document creation
- Agent productivity improvements

## Technical Considerations

### Scalability
- Design database queries to handle large lead datasets
- Implement pagination for lead history
- Consider caching strategies for frequently accessed data

### Security
- Implement proper access controls for document viewing
- Validate user permissions for lead data access
- Secure API endpoints with proper authentication

### Maintainability
- Follow existing code patterns and conventions
- Add comprehensive documentation for new features
- Implement proper error handling and logging

## Conclusion

This implementation plan provides a structured approach to transforming the RAG web app into a proactive AI copilot. By following this phased approach, we can ensure smooth development, testing, and deployment while maintaining system stability and user experience.

The plan emphasizes incremental development, thorough testing, and risk mitigation to ensure successful delivery of the Blueprint 2.0 features.
