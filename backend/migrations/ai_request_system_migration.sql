-- AI Request System Migration
-- Creates tables for the new AI request system with teams, pipelines, and deliverables

-- Create AI requests table
CREATE TABLE IF NOT EXISTS ai_requests_new (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    
    -- Request details
    team VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(20) DEFAULT 'text',
    audio_url VARCHAR(500),
    
    -- Template and branding
    template_id VARCHAR(100),
    brand_context JSONB DEFAULT '{}',
    
    -- Status and progress
    status VARCHAR(20) DEFAULT 'queued',
    priority INTEGER DEFAULT 5 CHECK (priority >= 1 AND priority <= 10),
    
    -- Timing
    eta TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Create indexes for AI requests
CREATE INDEX IF NOT EXISTS idx_ai_requests_user_id ON ai_requests_new(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_brokerage_id ON ai_requests_new(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_team ON ai_requests_new(team);
CREATE INDEX IF NOT EXISTS idx_ai_requests_status ON ai_requests_new(status);
CREATE INDEX IF NOT EXISTS idx_ai_requests_created_at ON ai_requests_new(created_at);
CREATE INDEX IF NOT EXISTS idx_ai_requests_eta ON ai_requests_new(eta);

-- Create AI request steps table
CREATE TABLE IF NOT EXISTS ai_request_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES ai_requests_new(id) ON DELETE CASCADE,
    
    -- Step details
    step VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    
    -- Timing
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    estimated_duration INTEGER, -- in seconds
    
    -- Results and metadata
    result TEXT,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for AI request steps
CREATE INDEX IF NOT EXISTS idx_ai_request_steps_request_id ON ai_request_steps(request_id);
CREATE INDEX IF NOT EXISTS idx_ai_request_steps_step ON ai_request_steps(step);
CREATE INDEX IF NOT EXISTS idx_ai_request_steps_status ON ai_request_steps(status);

-- Create deliverables table
CREATE TABLE IF NOT EXISTS deliverables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES ai_requests_new(id) ON DELETE CASCADE,
    
    -- Deliverable details
    type VARCHAR(20) NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    
    -- File information
    url VARCHAR(1000) NOT NULL,
    preview_url VARCHAR(1000),
    file_size INTEGER,
    mime_type VARCHAR(100),
    
    -- Status and metadata
    status VARCHAR(20) DEFAULT 'generating',
    metadata JSONB DEFAULT '{}',
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for deliverables
CREATE INDEX IF NOT EXISTS idx_deliverables_request_id ON deliverables(request_id);
CREATE INDEX IF NOT EXISTS idx_deliverables_type ON deliverables(type);
CREATE INDEX IF NOT EXISTS idx_deliverables_status ON deliverables(status);

-- Create templates table
CREATE TABLE IF NOT EXISTS templates (
    id VARCHAR(100) PRIMARY KEY,
    team VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Template configuration
    prompt_template TEXT NOT NULL,
    output_format VARCHAR(20) DEFAULT 'text',
    estimated_duration INTEGER DEFAULT 300, -- in seconds
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}',
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for templates
CREATE INDEX IF NOT EXISTS idx_templates_team ON templates(team);
CREATE INDEX IF NOT EXISTS idx_templates_is_active ON templates(is_active);

-- Create brand assets table
CREATE TABLE IF NOT EXISTS ai_brand_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    
    -- Asset details
    type VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- File information
    url VARCHAR(1000) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    
    -- Configuration
    config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for brand assets
CREATE INDEX IF NOT EXISTS idx_ai_brand_assets_brokerage_id ON ai_brand_assets(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_ai_brand_assets_type ON ai_brand_assets(type);
CREATE INDEX IF NOT EXISTS idx_ai_brand_assets_is_active ON ai_brand_assets(is_active);

-- Create AI request events table for real-time updates
CREATE TABLE IF NOT EXISTS ai_request_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES ai_requests_new(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Event details
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    
    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for AI request events
CREATE INDEX IF NOT EXISTS idx_ai_request_events_request_id ON ai_request_events(request_id);
CREATE INDEX IF NOT EXISTS idx_ai_request_events_user_id ON ai_request_events(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_request_events_created_at ON ai_request_events(created_at);

-- Insert default templates
INSERT INTO templates (id, team, name, description, prompt_template, output_format, estimated_duration) VALUES
-- Marketing templates
('postcard', 'marketing', 'Property Postcard', 'Create a stunning property postcard', 'Create a professional property postcard for: {content}', 'image', 300),
('email', 'marketing', 'Marketing Email', 'Professional property email campaign', 'Create a marketing email for: {content}', 'html', 240),
('social', 'marketing', 'Social Media Post', 'Engaging social media content', 'Create engaging social media content for: {content}', 'text', 180),
('brochure', 'marketing', 'Property Brochure', 'Comprehensive property brochure', 'Create a comprehensive property brochure for: {content}', 'pdf', 600),

-- Analytics templates
('cma', 'analytics', 'Comparative Market Analysis', 'Detailed CMA report', 'Create a comparative market analysis for: {content}', 'pdf', 900),
('market_report', 'analytics', 'Market Report', 'Comprehensive market analysis', 'Create a market report for: {content}', 'pdf', 720),
('valuation', 'analytics', 'Property Valuation', 'Professional property valuation', 'Create a property valuation for: {content}', 'pdf', 600),
('trends', 'analytics', 'Market Trends', 'Current market trends analysis', 'Analyze market trends for: {content}', 'pdf', 480),

-- Social media templates
('instagram', 'social', 'Instagram Post', 'Eye-catching Instagram content', 'Create Instagram content for: {content}', 'image', 240),
('facebook', 'social', 'Facebook Post', 'Engaging Facebook post', 'Create Facebook content for: {content}', 'text', 180),
('linkedin', 'social', 'LinkedIn Post', 'Professional LinkedIn content', 'Create LinkedIn content for: {content}', 'text', 240),
('story', 'social', 'Social Story', 'Quick social media story', 'Create a social media story for: {content}', 'image', 120),

-- Strategy templates
('business_plan', 'strategy', 'Business Plan', 'Strategic business planning', 'Create a business plan for: {content}', 'pdf', 1200),
('marketing_strategy', 'strategy', 'Marketing Strategy', 'Comprehensive marketing plan', 'Create a marketing strategy for: {content}', 'pdf', 900),
('client_strategy', 'strategy', 'Client Strategy', 'Client acquisition strategy', 'Create a client strategy for: {content}', 'pdf', 600),
('growth_plan', 'strategy', 'Growth Plan', 'Business growth planning', 'Create a growth plan for: {content}', 'pdf', 720),

-- Package templates
('premium', 'packages', 'Premium Package', 'Complete premium service package', 'Create a premium package for: {content}', 'pdf', 900),
('standard', 'packages', 'Standard Package', 'Standard service package', 'Create a standard package for: {content}', 'pdf', 600),
('basic', 'packages', 'Basic Package', 'Essential service package', 'Create a basic package for: {content}', 'pdf', 300),
('custom', 'packages', 'Custom Package', 'Tailored service package', 'Create a custom package for: {content}', 'pdf', 1200),

-- Transaction templates
('contract', 'transactions', 'Contract Review', 'Legal contract analysis', 'Review contract for: {content}', 'pdf', 600),
('negotiation', 'transactions', 'Negotiation Strategy', 'Deal negotiation planning', 'Create negotiation strategy for: {content}', 'pdf', 480),
('closing', 'transactions', 'Closing Process', 'Transaction closing management', 'Create closing process for: {content}', 'pdf', 360),
('compliance', 'transactions', 'Compliance Check', 'Regulatory compliance review', 'Perform compliance check for: {content}', 'pdf', 240)
ON CONFLICT (id) DO NOTHING;

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_ai_requests_updated_at BEFORE UPDATE ON ai_requests_new FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_deliverables_updated_at BEFORE UPDATE ON deliverables FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_templates_updated_at BEFORE UPDATE ON templates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brand_assets_updated_at BEFORE UPDATE ON brand_assets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add relationships to existing models (if needed)
-- Note: These would be added to the existing model files in Python

COMMENT ON TABLE ai_requests_new IS 'AI request processing and management with team-based pipelines';
COMMENT ON TABLE ai_request_steps IS 'Individual steps in the AI request pipeline';
COMMENT ON TABLE deliverables IS 'Deliverables generated by AI requests';
COMMENT ON TABLE templates IS 'Templates for different AI teams and request types';
COMMENT ON TABLE brand_assets IS 'Brand assets for personalization';
COMMENT ON TABLE ai_request_events IS 'Events for real-time updates via SSE/WebSocket';
