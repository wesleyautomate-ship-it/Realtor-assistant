-- =====================================================
-- BROKERAGE-CENTRIC SCHEMA MIGRATION
-- Phase 1: Foundation - Brokerage Architecture
-- =====================================================

-- Create brokerages table (Core entity for brokerage management)
CREATE TABLE IF NOT EXISTS brokerages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    license_number VARCHAR(100) UNIQUE,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    logo_url VARCHAR(500),
    branding_config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create team_performance table (Agent performance tracking)
CREATE TABLE IF NOT EXISTS team_performance (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    agent_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create knowledge_base table (Company policies and training materials)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    tags TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create brand_assets table (Logos, templates, and branding guidelines)
CREATE TABLE IF NOT EXISTS brand_assets (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL, -- 'logo', 'template', 'color_scheme', 'font'
    asset_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workflow_automation table (Task management and automation rules)
CREATE TABLE IF NOT EXISTS workflow_automation (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    trigger_type VARCHAR(50) NOT NULL, -- 'manual', 'scheduled', 'event_based'
    conditions JSONB DEFAULT '{}',
    actions JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create client_nurturing table (Communication sequences and templates)
CREATE TABLE IF NOT EXISTS client_nurturing (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    sequence_name VARCHAR(255) NOT NULL,
    description TEXT,
    steps JSONB DEFAULT '[]',
    triggers JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create compliance_rules table (Regulatory requirements and monitoring)
CREATE TABLE IF NOT EXISTS compliance_rules (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    rule_name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50) NOT NULL, -- 'rera', 'vat', 'contract', 'disclosure'
    description TEXT,
    conditions JSONB DEFAULT '{}',
    actions JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create agent_consistency_metrics table (Agent consistency tracking)
CREATE TABLE IF NOT EXISTS agent_consistency_metrics (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    consistency_score DECIMAL(5,2) NOT NULL,
    metrics JSONB DEFAULT '{}',
    period VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly'
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lead_retention_analytics table (Lead retention tracking)
CREATE TABLE IF NOT EXISTS lead_retention_analytics (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    lead_id INTEGER, -- Will reference leads table when it exists
    retention_score DECIMAL(5,2),
    touchpoints INTEGER DEFAULT 0,
    conversion_probability DECIMAL(5,2),
    last_contact_date TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create workflow_efficiency_metrics table (Workflow efficiency tracking)
CREATE TABLE IF NOT EXISTS workflow_efficiency_metrics (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    workflow_id INTEGER REFERENCES workflow_automation(id) ON DELETE CASCADE,
    efficiency_score DECIMAL(5,2),
    time_saved INTEGER, -- in minutes
    automation_rate DECIMAL(5,2),
    period_start DATE,
    period_end DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add brokerage_id to existing tables
ALTER TABLE users ADD COLUMN IF NOT EXISTS brokerage_id INTEGER REFERENCES brokerages(id);
ALTER TABLE properties ADD COLUMN IF NOT EXISTS brokerage_id INTEGER REFERENCES brokerages(id);
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS brokerage_id INTEGER REFERENCES brokerages(id);

-- Add brokerage_id to leads table if it exists
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'leads') THEN
        ALTER TABLE leads ADD COLUMN IF NOT EXISTS brokerage_id INTEGER REFERENCES brokerages(id);
    END IF;
END $$;

-- Add brokerage_id to notifications table if it exists
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'notifications') THEN
        ALTER TABLE notifications ADD COLUMN IF NOT EXISTS brokerage_id INTEGER REFERENCES brokerages(id);
    END IF;
END $$;

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_brokerages_name ON brokerages(name);
CREATE INDEX IF NOT EXISTS idx_brokerages_license ON brokerages(license_number);
CREATE INDEX IF NOT EXISTS idx_brokerages_active ON brokerages(is_active);

CREATE INDEX IF NOT EXISTS idx_team_performance_brokerage ON team_performance(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_team_performance_agent ON team_performance(agent_id);
CREATE INDEX IF NOT EXISTS idx_team_performance_period ON team_performance(period_start, period_end);

CREATE INDEX IF NOT EXISTS idx_knowledge_base_brokerage ON knowledge_base(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_category ON knowledge_base(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_active ON knowledge_base(is_active);

CREATE INDEX IF NOT EXISTS idx_brand_assets_brokerage ON brand_assets(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_brand_assets_type ON brand_assets(asset_type);

CREATE INDEX IF NOT EXISTS idx_workflow_automation_brokerage ON workflow_automation(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_workflow_automation_trigger ON workflow_automation(trigger_type);
CREATE INDEX IF NOT EXISTS idx_workflow_automation_active ON workflow_automation(is_active);

CREATE INDEX IF NOT EXISTS idx_client_nurturing_brokerage ON client_nurturing(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_client_nurturing_active ON client_nurturing(is_active);

CREATE INDEX IF NOT EXISTS idx_compliance_rules_brokerage ON compliance_rules(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_compliance_rules_type ON compliance_rules(rule_type);

CREATE INDEX IF NOT EXISTS idx_agent_consistency_agent ON agent_consistency_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_consistency_brokerage ON agent_consistency_metrics(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_agent_consistency_period ON agent_consistency_metrics(period);

CREATE INDEX IF NOT EXISTS idx_lead_retention_brokerage ON lead_retention_analytics(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_lead_retention_lead ON lead_retention_analytics(lead_id);

CREATE INDEX IF NOT EXISTS idx_workflow_efficiency_brokerage ON workflow_efficiency_metrics(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_workflow_efficiency_workflow ON workflow_efficiency_metrics(workflow_id);

-- Create composite indexes for analytics queries
CREATE INDEX IF NOT EXISTS idx_team_performance_analytics ON team_performance(brokerage_id, agent_id, period_start);
CREATE INDEX IF NOT EXISTS idx_agent_consistency_analytics ON agent_consistency_metrics(brokerage_id, period, calculated_at);
CREATE INDEX IF NOT EXISTS idx_lead_retention_analytics_composite ON lead_retention_analytics(brokerage_id, created_at);

-- Add updated_at triggers for tables that need them
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_brokerages_updated_at BEFORE UPDATE ON brokerages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_workflow_automation_updated_at BEFORE UPDATE ON workflow_automation FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_client_nurturing_updated_at BEFORE UPDATE ON client_nurturing FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_compliance_rules_updated_at BEFORE UPDATE ON compliance_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_lead_retention_analytics_updated_at BEFORE UPDATE ON lead_retention_analytics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default brokerage for existing users
INSERT INTO brokerages (name, license_number, address, phone, email, website, branding_config, is_active)
VALUES (
    'Default Brokerage',
    'DEFAULT-001',
    'Dubai, UAE',
    '+971-XX-XXXXXXX',
    'admin@defaultbrokerage.com',
    'https://defaultbrokerage.com',
    '{"primary_color": "#1976d2", "secondary_color": "#424242", "logo_position": "top_left"}',
    TRUE
) ON CONFLICT (license_number) DO NOTHING;

-- Update existing users to belong to default brokerage
UPDATE users SET brokerage_id = (SELECT id FROM brokerages WHERE license_number = 'DEFAULT-001' LIMIT 1)
WHERE brokerage_id IS NULL;

-- Update existing properties to belong to default brokerage
UPDATE properties SET brokerage_id = (SELECT id FROM brokerages WHERE license_number = 'DEFAULT-001' LIMIT 1)
WHERE brokerage_id IS NULL;

-- Update existing conversations to belong to default brokerage
UPDATE conversations SET brokerage_id = (SELECT id FROM brokerages WHERE license_number = 'DEFAULT-001' LIMIT 1)
WHERE brokerage_id IS NULL;

-- Add comments for documentation
COMMENT ON TABLE brokerages IS 'Central entity for brokerage management and branding';
COMMENT ON TABLE team_performance IS 'Agent performance tracking and analytics';
COMMENT ON TABLE knowledge_base IS 'Company policies, training materials, and best practices';
COMMENT ON TABLE brand_assets IS 'Logos, templates, and branding guidelines';
COMMENT ON TABLE workflow_automation IS 'Task management and automation rules';
COMMENT ON TABLE client_nurturing IS 'Communication sequences and templates for lead nurturing';
COMMENT ON TABLE compliance_rules IS 'Regulatory requirements and compliance monitoring';
COMMENT ON TABLE agent_consistency_metrics IS 'Agent consistency tracking and scoring';
COMMENT ON TABLE lead_retention_analytics IS 'Lead retention tracking and conversion analytics';
COMMENT ON TABLE workflow_efficiency_metrics IS 'Workflow efficiency tracking and optimization metrics';
