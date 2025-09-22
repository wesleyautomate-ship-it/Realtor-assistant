-- ============================================================
-- AI ASSISTANT SCHEMA MIGRATION
-- Phase 2: AI-Powered Assistant Core
-- ============================================================

-- AI Requests Table
-- Stores all AI requests from agents with processing status
CREATE TABLE IF NOT EXISTS ai_requests (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    request_type VARCHAR(50) NOT NULL, -- 'cma', 'presentation', 'marketing', 'compliance', 'general'
    request_content TEXT NOT NULL, -- Original request text/voice transcription
    request_metadata JSONB DEFAULT '{}', -- Additional request context
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'ai_complete', 'human_review', 'completed', 'failed'
    priority VARCHAR(10) DEFAULT 'normal', -- 'low', 'normal', 'high', 'urgent'
    ai_response TEXT, -- AI-generated response
    ai_confidence DECIMAL(3,2), -- AI confidence score (0.00-1.00)
    human_expert_id INTEGER REFERENCES users(id), -- Assigned human expert
    human_review TEXT, -- Human expert review/refinement
    human_rating INTEGER CHECK (human_rating >= 1 AND human_rating <= 5), -- Quality rating
    final_output TEXT, -- Final deliverable content
    output_format VARCHAR(20) DEFAULT 'text', -- 'text', 'pdf', 'presentation', 'email', 'social'
    estimated_completion TIMESTAMP,
    actual_completion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Human Experts Table
-- Manages the network of human experts who review AI output
CREATE TABLE IF NOT EXISTS human_experts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expertise_area VARCHAR(100) NOT NULL, -- 'market_analysis', 'presentations', 'compliance', 'marketing', 'general'
    availability_status VARCHAR(20) DEFAULT 'available', -- 'available', 'busy', 'offline'
    max_concurrent_tasks INTEGER DEFAULT 3,
    rating DECIMAL(3,2) DEFAULT 5.00, -- Average rating (1.00-5.00)
    completed_tasks INTEGER DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0.00,
    specializations TEXT[], -- Array of specializations
    languages TEXT[] DEFAULT ARRAY['English'], -- Languages spoken
    timezone VARCHAR(50) DEFAULT 'Asia/Dubai',
    working_hours JSONB DEFAULT '{"start": "09:00", "end": "18:00"}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content Deliverables Table
-- Stores the final content generated for requests
CREATE TABLE IF NOT EXISTS content_deliverables (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES ai_requests(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL, -- 'cma', 'presentation', 'email', 'social_post', 'document'
    file_path VARCHAR(500), -- Path to generated file
    content_data TEXT, -- Actual content data
    file_size INTEGER, -- File size in bytes
    mime_type VARCHAR(100), -- MIME type of the content
    branding_applied BOOLEAN DEFAULT FALSE,
    branding_config JSONB DEFAULT '{}', -- Branding configuration used
    quality_score DECIMAL(3,2), -- Quality assessment score
    client_feedback TEXT, -- Feedback from the requesting agent
    download_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT FALSE, -- Whether content can be shared
    expires_at TIMESTAMP, -- Content expiration date
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Voice Requests Table
-- Handles voice-to-text processing and audio file management
CREATE TABLE IF NOT EXISTS voice_requests (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    audio_file_path VARCHAR(500) NOT NULL, -- Path to audio file
    audio_duration INTEGER, -- Duration in seconds
    audio_format VARCHAR(20), -- 'mp3', 'wav', 'm4a', etc.
    file_size INTEGER, -- File size in bytes
    transcription TEXT, -- Voice-to-text transcription
    transcription_confidence DECIMAL(3,2), -- Transcription confidence score
    processed_request TEXT, -- Processed/cleaned request text
    language_detected VARCHAR(10) DEFAULT 'en', -- Detected language
    processing_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'transcribing', 'processed', 'failed'
    error_message TEXT, -- Error message if processing failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Task Automation Table
-- Manages automated task execution and workflow management
CREATE TABLE IF NOT EXISTS task_automation (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL, -- 'follow_up', 'report_generation', 'client_communication', 'data_entry'
    task_name VARCHAR(255) NOT NULL,
    task_description TEXT,
    automation_level VARCHAR(20) DEFAULT 'semi', -- 'full', 'semi', 'manual'
    trigger_conditions JSONB DEFAULT '{}', -- Conditions that trigger the task
    execution_schedule JSONB DEFAULT '{}', -- When/how often to execute
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'paused', 'completed', 'failed'
    last_execution TIMESTAMP,
    next_execution TIMESTAMP,
    execution_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00, -- Success rate percentage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Smart Nurturing Sequences Table
-- Manages automated client communication sequences
CREATE TABLE IF NOT EXISTS smart_nurturing_sequences (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    sequence_name VARCHAR(255) NOT NULL,
    sequence_type VARCHAR(50) NOT NULL, -- 'lead_nurturing', 'client_retention', 'follow_up', 'marketing'
    description TEXT,
    triggers JSONB DEFAULT '{}', -- Conditions that start the sequence
    steps JSONB DEFAULT '[]', -- Sequence steps with timing and content
    target_audience JSONB DEFAULT '{}', -- Who this sequence targets
    is_active BOOLEAN DEFAULT TRUE,
    performance_metrics JSONB DEFAULT '{}', -- Success rates, conversion metrics
    total_sent INTEGER DEFAULT 0,
    total_opened INTEGER DEFAULT 0,
    total_clicked INTEGER DEFAULT 0,
    total_converted INTEGER DEFAULT 0,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dubai Property Data Table
-- Stores integrated Dubai real estate data
CREATE TABLE IF NOT EXISTS dubai_property_data (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    rera_number VARCHAR(50) UNIQUE, -- RERA registration number
    property_type VARCHAR(50), -- 'apartment', 'villa', 'townhouse', 'office', 'retail'
    location_area VARCHAR(100), -- 'Dubai Marina', 'Palm Jumeirah', etc.
    market_data JSONB DEFAULT '{}', -- Market trends, pricing data
    price_history JSONB DEFAULT '[]', -- Historical price data
    neighborhood_data JSONB DEFAULT '{}', -- Area amenities, demographics
    rera_compliance_status VARCHAR(20) DEFAULT 'unknown', -- 'compliant', 'non_compliant', 'unknown'
    last_market_update TIMESTAMP,
    data_source VARCHAR(100), -- Source of the data
    data_quality_score DECIMAL(3,2) DEFAULT 1.00, -- Data quality assessment
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RERA Compliance Data Table
-- Tracks RERA compliance status and requirements
CREATE TABLE IF NOT EXISTS rera_compliance_data (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    compliance_status VARCHAR(20) DEFAULT 'pending', -- 'compliant', 'non_compliant', 'pending', 'exempt'
    compliance_type VARCHAR(50), -- 'listing', 'transaction', 'disclosure', 'documentation'
    required_documents JSONB DEFAULT '[]', -- List of required documents
    submitted_documents JSONB DEFAULT '[]', -- List of submitted documents
    compliance_score DECIMAL(3,2), -- Compliance score (0.00-1.00)
    last_check TIMESTAMP,
    next_check TIMESTAMP,
    compliance_notes TEXT,
    regulatory_updates JSONB DEFAULT '[]', -- Recent regulatory changes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Retention Analytics Table
-- Tracks lead retention and conversion metrics
CREATE TABLE IF NOT EXISTS retention_analytics (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER NOT NULL REFERENCES brokerages(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL, -- 'lead_conversion', 'client_retention', 'follow_up_success'
    metric_value DECIMAL(10,2) NOT NULL,
    metric_unit VARCHAR(20), -- 'percentage', 'count', 'days', 'currency'
    period VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly', 'quarterly'
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    benchmark_value DECIMAL(10,2), -- Industry benchmark for comparison
    trend_direction VARCHAR(10), -- 'up', 'down', 'stable'
    trend_percentage DECIMAL(5,2), -- Percentage change from previous period
    metadata JSONB DEFAULT '{}', -- Additional metric context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_ai_requests_agent_id ON ai_requests(agent_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_brokerage_id ON ai_requests(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_status ON ai_requests(status);
CREATE INDEX IF NOT EXISTS idx_ai_requests_created_at ON ai_requests(created_at);
CREATE INDEX IF NOT EXISTS idx_ai_requests_request_type ON ai_requests(request_type);

CREATE INDEX IF NOT EXISTS idx_human_experts_user_id ON human_experts(user_id);
CREATE INDEX IF NOT EXISTS idx_human_experts_expertise_area ON human_experts(expertise_area);
CREATE INDEX IF NOT EXISTS idx_human_experts_availability_status ON human_experts(availability_status);
CREATE INDEX IF NOT EXISTS idx_human_experts_rating ON human_experts(rating);

CREATE INDEX IF NOT EXISTS idx_content_deliverables_request_id ON content_deliverables(request_id);
CREATE INDEX IF NOT EXISTS idx_content_deliverables_content_type ON content_deliverables(content_type);
CREATE INDEX IF NOT EXISTS idx_content_deliverables_created_at ON content_deliverables(created_at);

CREATE INDEX IF NOT EXISTS idx_voice_requests_agent_id ON voice_requests(agent_id);
CREATE INDEX IF NOT EXISTS idx_voice_requests_processing_status ON voice_requests(processing_status);
CREATE INDEX IF NOT EXISTS idx_voice_requests_created_at ON voice_requests(created_at);

CREATE INDEX IF NOT EXISTS idx_task_automation_agent_id ON task_automation(agent_id);
CREATE INDEX IF NOT EXISTS idx_task_automation_brokerage_id ON task_automation(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_task_automation_status ON task_automation(status);
CREATE INDEX IF NOT EXISTS idx_task_automation_next_execution ON task_automation(next_execution);

CREATE INDEX IF NOT EXISTS idx_smart_nurturing_brokerage_id ON smart_nurturing_sequences(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_smart_nurturing_is_active ON smart_nurturing_sequences(is_active);
CREATE INDEX IF NOT EXISTS idx_smart_nurturing_sequence_type ON smart_nurturing_sequences(sequence_type);

CREATE INDEX IF NOT EXISTS idx_dubai_property_data_rera_number ON dubai_property_data(rera_number);
CREATE INDEX IF NOT EXISTS idx_dubai_property_data_property_id ON dubai_property_data(property_id);
CREATE INDEX IF NOT EXISTS idx_dubai_property_data_location_area ON dubai_property_data(location_area);

CREATE INDEX IF NOT EXISTS idx_rera_compliance_property_id ON rera_compliance_data(property_id);
CREATE INDEX IF NOT EXISTS idx_rera_compliance_brokerage_id ON rera_compliance_data(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_rera_compliance_status ON rera_compliance_data(compliance_status);

CREATE INDEX IF NOT EXISTS idx_retention_analytics_brokerage_id ON retention_analytics(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_retention_analytics_metric_name ON retention_analytics(metric_name);
CREATE INDEX IF NOT EXISTS idx_retention_analytics_period ON retention_analytics(period);
CREATE INDEX IF NOT EXISTS idx_retention_analytics_period_start ON retention_analytics(period_start);

-- Add foreign key constraints
ALTER TABLE ai_requests ADD CONSTRAINT fk_ai_requests_agent_id FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE ai_requests ADD CONSTRAINT fk_ai_requests_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;
ALTER TABLE ai_requests ADD CONSTRAINT fk_ai_requests_human_expert_id FOREIGN KEY (human_expert_id) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE human_experts ADD CONSTRAINT fk_human_experts_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE content_deliverables ADD CONSTRAINT fk_content_deliverables_request_id FOREIGN KEY (request_id) REFERENCES ai_requests(id) ON DELETE CASCADE;

ALTER TABLE voice_requests ADD CONSTRAINT fk_voice_requests_agent_id FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE voice_requests ADD CONSTRAINT fk_voice_requests_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE task_automation ADD CONSTRAINT fk_task_automation_agent_id FOREIGN KEY (agent_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE task_automation ADD CONSTRAINT fk_task_automation_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE smart_nurturing_sequences ADD CONSTRAINT fk_smart_nurturing_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;
ALTER TABLE smart_nurturing_sequences ADD CONSTRAINT fk_smart_nurturing_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE dubai_property_data ADD CONSTRAINT fk_dubai_property_data_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE;

ALTER TABLE rera_compliance_data ADD CONSTRAINT fk_rera_compliance_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE;
ALTER TABLE rera_compliance_data ADD CONSTRAINT fk_rera_compliance_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE retention_analytics ADD CONSTRAINT fk_retention_analytics_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

-- Insert default human expert (system admin as fallback)
INSERT INTO human_experts (user_id, expertise_area, availability_status, max_concurrent_tasks, rating, specializations, is_active)
SELECT 
    u.id,
    'general',
    'available',
    5,
    5.00,
    ARRAY['general_real_estate', 'market_analysis', 'presentations', 'compliance'],
    TRUE
FROM users u 
WHERE u.role = 'admin' 
AND NOT EXISTS (
    SELECT 1 FROM human_experts he WHERE he.user_id = u.id
)
LIMIT 1;

-- Create updated_at trigger function if it doesn't exist
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_ai_requests_updated_at BEFORE UPDATE ON ai_requests FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_human_experts_updated_at BEFORE UPDATE ON human_experts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_content_deliverables_updated_at BEFORE UPDATE ON content_deliverables FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_voice_requests_updated_at BEFORE UPDATE ON voice_requests FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_task_automation_updated_at BEFORE UPDATE ON task_automation FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_smart_nurturing_sequences_updated_at BEFORE UPDATE ON smart_nurturing_sequences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_dubai_property_data_updated_at BEFORE UPDATE ON dubai_property_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_rera_compliance_data_updated_at BEFORE UPDATE ON rera_compliance_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;
