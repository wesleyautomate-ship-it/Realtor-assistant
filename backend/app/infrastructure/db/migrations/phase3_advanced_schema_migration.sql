-- ============================================================
-- PHASE 3 ADVANCED SCHEMA MIGRATION
-- Advanced Analytics, Dubai Data Integration & Developer Panel
-- ============================================================

-- Predictive Performance Models Table
-- Stores ML models for predicting agent and brokerage performance
CREATE TABLE IF NOT EXISTS predictive_performance_models (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    model_type VARCHAR(50) NOT NULL, -- 'agent_performance', 'lead_conversion', 'market_trend', 'client_retention'
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(20) DEFAULT '1.0.0',
    parameters JSONB DEFAULT '{}', -- Model hyperparameters and configuration
    training_data_period_start DATE NOT NULL,
    training_data_period_end DATE NOT NULL,
    accuracy_score DECIMAL(5,4), -- Model accuracy (0.0000-1.0000)
    precision_score DECIMAL(5,4), -- Model precision
    recall_score DECIMAL(5,4), -- Model recall
    f1_score DECIMAL(5,4), -- Model F1 score
    model_file_path VARCHAR(500), -- Path to saved model file
    feature_importance JSONB DEFAULT '{}', -- Feature importance scores
    is_active BOOLEAN DEFAULT TRUE,
    last_trained TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Benchmarking Data Table
-- Stores industry benchmarks and performance comparisons
CREATE TABLE IF NOT EXISTS benchmarking_data (
    id SERIAL PRIMARY KEY,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    benchmark_type VARCHAR(50) NOT NULL, -- 'agent_performance', 'lead_conversion', 'client_retention', 'market_share'
    metric_name VARCHAR(100) NOT NULL,
    industry_standard DECIMAL(10,2), -- Industry average/standard
    top_performer_standard DECIMAL(10,2), -- Top 10% performer standard
    brokerage_performance DECIMAL(10,2), -- Current brokerage performance
    performance_gap DECIMAL(10,2), -- Gap from industry standard
    percentile_ranking INTEGER, -- Percentile ranking (1-100)
    benchmark_period_start DATE NOT NULL,
    benchmark_period_end DATE NOT NULL,
    data_source VARCHAR(100), -- Source of benchmark data
    confidence_level DECIMAL(3,2) DEFAULT 0.95, -- Statistical confidence
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dubai Market Data Integration Table
-- Stores integrated Dubai real estate market data from multiple sources
CREATE TABLE IF NOT EXISTS dubai_market_data (
    id SERIAL PRIMARY KEY,
    area_name VARCHAR(100) NOT NULL, -- 'Dubai Marina', 'Palm Jumeirah', etc.
    property_type VARCHAR(50) NOT NULL, -- 'apartment', 'villa', 'townhouse', 'office', 'retail'
    data_type VARCHAR(50) NOT NULL, -- 'price_per_sqft', 'rental_yield', 'occupancy_rate', 'transaction_volume'
    data_value DECIMAL(15,2) NOT NULL,
    data_unit VARCHAR(20), -- 'AED', 'percentage', 'count', 'sqft'
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    data_source VARCHAR(100) NOT NULL, -- 'RERA', 'Dubai Land Department', 'Property Finder', 'Bayut'
    data_quality_score DECIMAL(3,2) DEFAULT 1.00, -- Data quality assessment
    is_verified BOOLEAN DEFAULT FALSE, -- Data verification status
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RERA Integration Data Table
-- Stores RERA-specific data and compliance information
CREATE TABLE IF NOT EXISTS rera_integration_data (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    rera_number VARCHAR(50) UNIQUE NOT NULL,
    developer_name VARCHAR(255),
    project_name VARCHAR(255),
    completion_status VARCHAR(50), -- 'completed', 'under_construction', 'planned'
    handover_date DATE,
    rera_approval_date DATE,
    escrow_account_number VARCHAR(100),
    escrow_bank VARCHAR(255),
    payment_plan JSONB DEFAULT '{}', -- Payment plan details
    amenities JSONB DEFAULT '[]', -- Project amenities
    nearby_facilities JSONB DEFAULT '[]', -- Nearby facilities and services
    transportation_links JSONB DEFAULT '[]', -- Metro, bus, road connections
    compliance_status VARCHAR(20) DEFAULT 'compliant', -- 'compliant', 'non_compliant', 'pending'
    last_rera_check TIMESTAMP,
    rera_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Performance Metrics Table
-- Stores system-wide performance and usage metrics
CREATE TABLE IF NOT EXISTS system_performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_category VARCHAR(50) NOT NULL, -- 'api_performance', 'database_performance', 'ai_processing', 'user_activity'
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metric_unit VARCHAR(20), -- 'milliseconds', 'requests_per_second', 'percentage', 'count'
    measurement_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSONB DEFAULT '{}', -- Additional context data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Activity Analytics Table
-- Stores detailed user activity and behavior analytics
CREATE TABLE IF NOT EXISTS user_activity_analytics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    brokerage_id INTEGER REFERENCES brokerages(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- 'login', 'request_creation', 'content_download', 'expert_review'
    activity_details JSONB DEFAULT '{}', -- Detailed activity information
    session_id VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_type VARCHAR(50), -- 'desktop', 'mobile', 'tablet'
    browser_type VARCHAR(50),
    duration_seconds INTEGER, -- Activity duration
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Processing Analytics Table
-- Stores AI processing performance and quality metrics
CREATE TABLE IF NOT EXISTS ai_processing_analytics (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES ai_requests(id) ON DELETE CASCADE,
    processing_stage VARCHAR(50) NOT NULL, -- 'request_analysis', 'ai_generation', 'human_review', 'content_delivery'
    processing_time_ms INTEGER NOT NULL, -- Processing time in milliseconds
    ai_model_used VARCHAR(100),
    ai_confidence_score DECIMAL(3,2),
    human_review_time_ms INTEGER,
    human_rating INTEGER CHECK (human_rating >= 1 AND human_rating <= 5),
    quality_score DECIMAL(3,2),
    error_occurred BOOLEAN DEFAULT FALSE,
    error_type VARCHAR(100),
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Multi-Brokerage Analytics Table
-- Stores cross-brokerage analytics for system-wide insights
CREATE TABLE IF NOT EXISTS multi_brokerage_analytics (
    id SERIAL PRIMARY KEY,
    analytics_type VARCHAR(50) NOT NULL, -- 'system_usage', 'feature_adoption', 'performance_comparison', 'market_insights'
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    metric_unit VARCHAR(20),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    brokerage_count INTEGER, -- Number of brokerages included
    total_users INTEGER, -- Total users across brokerages
    additional_metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Developer Panel Settings Table
-- Stores developer panel configuration and preferences
CREATE TABLE IF NOT EXISTS developer_panel_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    setting_category VARCHAR(50) NOT NULL, -- 'monitoring', 'alerts', 'analytics', 'system_control'
    setting_name VARCHAR(100) NOT NULL,
    setting_value JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, setting_category, setting_name)
);

-- System Alerts Table
-- Stores system alerts and notifications for developers
CREATE TABLE IF NOT EXISTS system_alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL, -- 'error', 'warning', 'info', 'performance'
    alert_category VARCHAR(50) NOT NULL, -- 'system', 'database', 'ai_processing', 'user_activity'
    alert_title VARCHAR(255) NOT NULL,
    alert_message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    affected_components JSONB DEFAULT '[]', -- List of affected system components
    alert_data JSONB DEFAULT '{}', -- Additional alert context
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by INTEGER REFERENCES users(id),
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_predictive_models_brokerage_id ON predictive_performance_models(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_predictive_models_model_type ON predictive_performance_models(model_type);
CREATE INDEX IF NOT EXISTS idx_predictive_models_is_active ON predictive_performance_models(is_active);
CREATE INDEX IF NOT EXISTS idx_predictive_models_last_trained ON predictive_performance_models(last_trained);

CREATE INDEX IF NOT EXISTS idx_benchmarking_brokerage_id ON benchmarking_data(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_benchmarking_benchmark_type ON benchmarking_data(benchmark_type);
CREATE INDEX IF NOT EXISTS idx_benchmarking_period_start ON benchmarking_data(benchmark_period_start);

CREATE INDEX IF NOT EXISTS idx_dubai_market_area_name ON dubai_market_data(area_name);
CREATE INDEX IF NOT EXISTS idx_dubai_market_property_type ON dubai_market_data(property_type);
CREATE INDEX IF NOT EXISTS idx_dubai_market_data_type ON dubai_market_data(data_type);
CREATE INDEX IF NOT EXISTS idx_dubai_market_period_start ON dubai_market_data(period_start);

CREATE INDEX IF NOT EXISTS idx_rera_integration_property_id ON rera_integration_data(property_id);
CREATE INDEX IF NOT EXISTS idx_rera_integration_rera_number ON rera_integration_data(rera_number);
CREATE INDEX IF NOT EXISTS idx_rera_integration_compliance_status ON rera_integration_data(compliance_status);

CREATE INDEX IF NOT EXISTS idx_system_performance_metric_category ON system_performance_metrics(metric_category);
CREATE INDEX IF NOT EXISTS idx_system_performance_measurement_timestamp ON system_performance_metrics(measurement_timestamp);

CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_brokerage_id ON user_activity_analytics(brokerage_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_activity_type ON user_activity_analytics(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activity_created_at ON user_activity_analytics(created_at);

CREATE INDEX IF NOT EXISTS idx_ai_processing_request_id ON ai_processing_analytics(request_id);
CREATE INDEX IF NOT EXISTS idx_ai_processing_stage ON ai_processing_analytics(processing_stage);
CREATE INDEX IF NOT EXISTS idx_ai_processing_created_at ON ai_processing_analytics(created_at);

CREATE INDEX IF NOT EXISTS idx_multi_brokerage_analytics_type ON multi_brokerage_analytics(analytics_type);
CREATE INDEX IF NOT EXISTS idx_multi_brokerage_period_start ON multi_brokerage_analytics(period_start);

CREATE INDEX IF NOT EXISTS idx_developer_settings_user_id ON developer_panel_settings(user_id);
CREATE INDEX IF NOT EXISTS idx_developer_settings_category ON developer_panel_settings(setting_category);

CREATE INDEX IF NOT EXISTS idx_system_alerts_alert_type ON system_alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_system_alerts_severity ON system_alerts(severity);
CREATE INDEX IF NOT EXISTS idx_system_alerts_is_resolved ON system_alerts(is_resolved);
CREATE INDEX IF NOT EXISTS idx_system_alerts_created_at ON system_alerts(created_at);

-- Add foreign key constraints
ALTER TABLE predictive_performance_models ADD CONSTRAINT fk_predictive_models_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE benchmarking_data ADD CONSTRAINT fk_benchmarking_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE rera_integration_data ADD CONSTRAINT fk_rera_integration_property_id FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE;

ALTER TABLE user_activity_analytics ADD CONSTRAINT fk_user_activity_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_activity_analytics ADD CONSTRAINT fk_user_activity_brokerage_id FOREIGN KEY (brokerage_id) REFERENCES brokerages(id) ON DELETE CASCADE;

ALTER TABLE ai_processing_analytics ADD CONSTRAINT fk_ai_processing_request_id FOREIGN KEY (request_id) REFERENCES ai_requests(id) ON DELETE CASCADE;

ALTER TABLE developer_panel_settings ADD CONSTRAINT fk_developer_settings_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE system_alerts ADD CONSTRAINT fk_system_alerts_resolved_by FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL;

-- Create updated_at trigger function if it doesn't exist
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_predictive_models_updated_at BEFORE UPDATE ON predictive_performance_models FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_benchmarking_data_updated_at BEFORE UPDATE ON benchmarking_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_rera_integration_updated_at BEFORE UPDATE ON rera_integration_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_developer_settings_updated_at BEFORE UPDATE ON developer_panel_settings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_system_alerts_updated_at BEFORE UPDATE ON system_alerts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample Dubai market data
INSERT INTO dubai_market_data (area_name, property_type, data_type, data_value, data_unit, period_start, period_end, data_source, is_verified) VALUES
('Dubai Marina', 'apartment', 'price_per_sqft', 1200.00, 'AED', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Dubai Marina', 'apartment', 'rental_yield', 6.5, 'percentage', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Palm Jumeirah', 'villa', 'price_per_sqft', 2500.00, 'AED', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Palm Jumeirah', 'villa', 'rental_yield', 5.2, 'percentage', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Downtown Dubai', 'apartment', 'price_per_sqft', 1800.00, 'AED', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Downtown Dubai', 'apartment', 'rental_yield', 7.1, 'percentage', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Business Bay', 'apartment', 'price_per_sqft', 1100.00, 'AED', '2024-01-01', '2024-01-31', 'RERA', TRUE),
('Business Bay', 'apartment', 'rental_yield', 6.8, 'percentage', '2024-01-01', '2024-01-31', 'RERA', TRUE);

-- Insert sample system performance metrics
INSERT INTO system_performance_metrics (metric_category, metric_name, metric_value, metric_unit, additional_data) VALUES
('api_performance', 'average_response_time', 150.5, 'milliseconds', '{"endpoint": "ai-assistant/requests"}'),
('database_performance', 'query_execution_time', 25.3, 'milliseconds', '{"table": "ai_requests"}'),
('ai_processing', 'average_processing_time', 4500.0, 'milliseconds', '{"model": "gpt-4"}'),
('user_activity', 'active_users_per_hour', 45.0, 'count', '{"period": "peak_hours"}');

-- Insert sample multi-brokerage analytics
INSERT INTO multi_brokerage_analytics (analytics_type, metric_name, metric_value, metric_unit, period_start, period_end, brokerage_count, total_users, additional_metrics) VALUES
('system_usage', 'total_ai_requests', 1250.0, 'count', '2024-01-01', '2024-01-31', 5, 45, '{"average_per_brokerage": 250}'),
('feature_adoption', 'voice_requests_adoption', 78.5, 'percentage', '2024-01-01', '2024-01-31', 5, 45, '{"brokerages_using_feature": 4}'),
('performance_comparison', 'average_completion_time', 2.3, 'hours', '2024-01-01', '2024-01-31', 5, 45, '{"best_performing_brokerage": "brokerage_1"}');

COMMIT;
