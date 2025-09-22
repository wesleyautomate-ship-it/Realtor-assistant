-- Voice AI Schema Migration
-- Adds tables for voice processing, content generation, and content management
-- Run this migration after the existing schema is in place

-- =============================================
-- VOICE PROCESSING TABLES
-- =============================================

-- Voice Sessions table - tracks voice interaction sessions
CREATE TABLE IF NOT EXISTS voice_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    session_id VARCHAR(100) NOT NULL UNIQUE,
    transcript TEXT,
    intent VARCHAR(50),
    entities JSONB DEFAULT '{}',
    processing_type VARCHAR(20) DEFAULT 'realtime', -- 'realtime' or 'batch'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Voice Requests table - tracks individual voice requests
CREATE TABLE IF NOT EXISTS voice_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES voice_sessions(id),
    user_id UUID NOT NULL,
    audio_file_path TEXT,
    transcript TEXT,
    intent VARCHAR(50),
    entities JSONB DEFAULT '{}',
    processing_type VARCHAR(20) NOT NULL, -- 'realtime' or 'batch'
    status VARCHAR(20) DEFAULT 'queued', -- 'queued', 'processing', 'completed', 'failed'
    response_data JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- =============================================
-- CONTENT MANAGEMENT SYSTEM
-- =============================================

-- Content Templates table - stores template definitions
CREATE TABLE IF NOT EXISTS content_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_type VARCHAR(50) NOT NULL, -- 'cma', 'just_listed', 'newsletter', etc.
    template_name VARCHAR(100) NOT NULL,
    template_description TEXT,
    template_prompt TEXT NOT NULL,
    template_config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_by UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Generated Content table - stores AI-generated content
CREATE TABLE IF NOT EXISTS generated_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    voice_request_id UUID REFERENCES voice_requests(id),
    template_id UUID REFERENCES content_templates(id),
    user_id UUID NOT NULL,
    template_type VARCHAR(50) NOT NULL,
    content_data JSONB NOT NULL,
    property_data JSONB DEFAULT '{}',
    user_preferences JSONB DEFAULT '{}',
    approval_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'published'
    approved_by UUID,
    approved_at TIMESTAMP,
    published_at TIMESTAMP,
    published_to JSONB DEFAULT '[]', -- Array of channels where content was published
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Content Versions table - tracks content revisions
CREATE TABLE IF NOT EXISTS content_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES generated_content(id),
    version_number INTEGER NOT NULL,
    content_data JSONB NOT NULL,
    change_description TEXT,
    created_by UUID,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content Publishing Log table - tracks where content was published
CREATE TABLE IF NOT EXISTS content_publishing_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES generated_content(id),
    channel VARCHAR(50) NOT NULL, -- 'social_media', 'email', 'website', 'print'
    channel_details JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'published', 'failed'
    published_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- USER PREFERENCES AND ONBOARDING
-- =============================================

-- User Preferences table - stores user onboarding and preferences
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    specialty VARCHAR(50) NOT NULL, -- 'residential', 'commercial', 'luxury', 'investment'
    workflow VARCHAR(50) NOT NULL, -- 'high_touch', 'automated', 'hybrid'
    preferred_templates JSONB DEFAULT '[]',
    notification_settings JSONB DEFAULT '{}',
    voice_settings JSONB DEFAULT '{}',
    content_preferences JSONB DEFAULT '{}',
    onboarding_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =============================================
-- AI REQUEST TRACKING (ENHANCED)
-- =============================================

-- AI Requests table - enhanced for voice processing
CREATE TABLE IF NOT EXISTS ai_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    request_type VARCHAR(50) NOT NULL,
    input_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'queued', -- 'queued', 'processing', 'completed', 'failed'
    result_data JSONB,
    processing_type VARCHAR(20) DEFAULT 'batch', -- 'realtime' or 'batch'
    voice_request_id UUID REFERENCES voice_requests(id),
    content_id UUID REFERENCES generated_content(id),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    processing_time_ms INTEGER
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Voice Sessions indexes
CREATE INDEX IF NOT EXISTS idx_voice_sessions_user_id ON voice_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_voice_sessions_session_id ON voice_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_voice_sessions_status ON voice_sessions(status);
CREATE INDEX IF NOT EXISTS idx_voice_sessions_created_at ON voice_sessions(created_at);

-- Voice Requests indexes
CREATE INDEX IF NOT EXISTS idx_voice_requests_user_id ON voice_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_voice_requests_session_id ON voice_requests(session_id);
CREATE INDEX IF NOT EXISTS idx_voice_requests_status ON voice_requests(status);
CREATE INDEX IF NOT EXISTS idx_voice_requests_processing_type ON voice_requests(processing_type);
CREATE INDEX IF NOT EXISTS idx_voice_requests_created_at ON voice_requests(created_at);

-- Content Templates indexes
CREATE INDEX IF NOT EXISTS idx_content_templates_type ON content_templates(template_type);
CREATE INDEX IF NOT EXISTS idx_content_templates_active ON content_templates(is_active);

-- Generated Content indexes
CREATE INDEX IF NOT EXISTS idx_generated_content_user_id ON generated_content(user_id);
CREATE INDEX IF NOT EXISTS idx_generated_content_template_type ON generated_content(template_type);
CREATE INDEX IF NOT EXISTS idx_generated_content_approval_status ON generated_content(approval_status);
CREATE INDEX IF NOT EXISTS idx_generated_content_created_at ON generated_content(created_at);

-- Content Versions indexes
CREATE INDEX IF NOT EXISTS idx_content_versions_content_id ON content_versions(content_id);
CREATE INDEX IF NOT EXISTS idx_content_versions_version_number ON content_versions(version_number);

-- Content Publishing Log indexes
CREATE INDEX IF NOT EXISTS idx_content_publishing_log_content_id ON content_publishing_log(content_id);
CREATE INDEX IF NOT EXISTS idx_content_publishing_log_channel ON content_publishing_log(channel);
CREATE INDEX IF NOT EXISTS idx_content_publishing_log_status ON content_publishing_log(status);

-- User Preferences indexes
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_user_preferences_specialty ON user_preferences(specialty);
CREATE INDEX IF NOT EXISTS idx_user_preferences_workflow ON user_preferences(workflow);

-- AI Requests indexes
CREATE INDEX IF NOT EXISTS idx_ai_requests_user_id ON ai_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_status ON ai_requests(status);
CREATE INDEX IF NOT EXISTS idx_ai_requests_processing_type ON ai_requests(processing_type);
CREATE INDEX IF NOT EXISTS idx_ai_requests_created_at ON ai_requests(created_at);

-- =============================================
-- INITIAL DATA SEEDING
-- =============================================

-- Insert default content templates
INSERT INTO content_templates (template_type, template_name, template_description, template_prompt) VALUES
('cma', 'Comparative Market Analysis', 'Generate comprehensive CMA reports with pricing strategies', 'Generate a comprehensive Comparative Market Analysis (CMA) for the following property...'),
('just_listed', 'Just Listed Marketing', 'Create compelling just listed marketing content', 'Create compelling "Just Listed" marketing content for the following property...'),
('just_sold', 'Just Sold Celebration', 'Generate just sold celebration content', 'Generate "Just Sold" celebration content for the following property...'),
('open_house', 'Open House Invitation', 'Create open house invitations and promotional materials', 'Create open house invitation and promotional materials for...'),
('newsletter', 'Market Newsletter', 'Generate market newsletters and client communications', 'Generate a market newsletter with the following content...'),
('investor_deck', 'Investment Presentation', 'Create investment presentations and property analysis', 'Create an investment presentation deck for the following property...'),
('brochure', 'Property Brochure', 'Generate property brochures and marketing materials', 'Generate a property brochure for the following property...'),
('social_banner', 'Social Media Banner', 'Create social media banners and graphics', 'Create social media banner content for the following property...'),
('story_content', 'Social Media Stories', 'Generate social media story content', 'Generate social media story content for the following property...')
ON CONFLICT DO NOTHING;

-- =============================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at columns
CREATE TRIGGER update_content_templates_updated_at BEFORE UPDATE ON content_templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_generated_content_updated_at BEFORE UPDATE ON generated_content FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- VIEWS FOR COMMON QUERIES
-- =============================================

-- View for active voice sessions
CREATE OR REPLACE VIEW active_voice_sessions AS
SELECT 
    vs.id,
    vs.user_id,
    vs.session_id,
    vs.transcript,
    vs.intent,
    vs.status,
    vs.created_at,
    COUNT(vr.id) as request_count
FROM voice_sessions vs
LEFT JOIN voice_requests vr ON vs.id = vr.session_id
WHERE vs.status = 'active'
GROUP BY vs.id, vs.user_id, vs.session_id, vs.transcript, vs.intent, vs.status, vs.created_at;

-- View for pending content approvals
CREATE OR REPLACE VIEW pending_content_approvals AS
SELECT 
    gc.id,
    gc.user_id,
    gc.template_type,
    gc.content_data,
    gc.created_at,
    ct.template_name,
    ct.template_description
FROM generated_content gc
JOIN content_templates ct ON gc.template_id = ct.id
WHERE gc.approval_status = 'pending'
ORDER BY gc.created_at DESC;

-- View for user content statistics
CREATE OR REPLACE VIEW user_content_stats AS
SELECT 
    user_id,
    COUNT(*) as total_content,
    COUNT(CASE WHEN approval_status = 'approved' THEN 1 END) as approved_content,
    COUNT(CASE WHEN approval_status = 'published' THEN 1 END) as published_content,
    COUNT(CASE WHEN template_type = 'cma' THEN 1 END) as cma_count,
    COUNT(CASE WHEN template_type = 'just_listed' THEN 1 END) as just_listed_count,
    COUNT(CASE WHEN template_type = 'newsletter' THEN 1 END) as newsletter_count
FROM generated_content
GROUP BY user_id;

-- =============================================
-- MIGRATION COMPLETION
-- =============================================

-- Log migration completion
INSERT INTO migration_log (migration_name, executed_at, status) 
VALUES ('voice_ai_schema_migration', NOW(), 'completed')
ON CONFLICT (migration_name) DO UPDATE SET 
    executed_at = NOW(), 
    status = 'completed';

-- Create migration log table if it doesn't exist
CREATE TABLE IF NOT EXISTS migration_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    migration_name VARCHAR(100) UNIQUE NOT NULL,
    executed_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'completed'
);

COMMENT ON TABLE voice_sessions IS 'Tracks voice interaction sessions for real estate agents';
COMMENT ON TABLE voice_requests IS 'Individual voice requests and their processing status';
COMMENT ON TABLE content_templates IS 'Template definitions for content generation';
COMMENT ON TABLE generated_content IS 'AI-generated content awaiting approval and publishing';
COMMENT ON TABLE content_versions IS 'Version history for generated content';
COMMENT ON TABLE content_publishing_log IS 'Log of content publishing to various channels';
COMMENT ON TABLE user_preferences IS 'User onboarding preferences and settings';
COMMENT ON TABLE ai_requests IS 'Enhanced AI request tracking for voice processing';
