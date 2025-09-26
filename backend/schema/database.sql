-- Core schema for PropertyPro AI (PostgreSQL compatible)
-- Minimal tables for properties, clients, transactions to satisfy CRUD

CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    property_type VARCHAR(50),
    price NUMERIC(15,2),
    location VARCHAR(255),
    area_sqft NUMERIC(10,2),
    bedrooms INTEGER,
    bathrooms INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    budget_min NUMERIC(12,2),
    budget_max NUMERIC(12,2),
    preferred_location VARCHAR(255),
    requirements TEXT,
    client_type VARCHAR(20) DEFAULT 'buyer',
    client_status VARCHAR(20) DEFAULT 'active',
    assigned_agent_id INTEGER,
    relationship_start_date DATE,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
    buyer_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    seller_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    agent_id INTEGER,
    transaction_type VARCHAR(20) NOT NULL,
    transaction_status VARCHAR(20) DEFAULT 'pending',
    offer_price NUMERIC(15,2),
    final_price NUMERIC(15,2),
    commission_rate NUMERIC(5,2),
    commission_amount NUMERIC(15,2),
    transaction_date DATE,
    closing_date DATE,
    contract_signed_date DATE,
    payment_terms JSONB,
    documents JSONB,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transaction_history (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(id) ON DELETE CASCADE,
    status_change VARCHAR(50) NOT NULL,
    previous_status VARCHAR(20),
    new_status VARCHAR(20),
    changed_by INTEGER,
    change_reason TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Orchestration tables
CREATE TABLE IF NOT EXISTS ai_tasks (
    id VARCHAR(64) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_type VARCHAR(64) NOT NULL,
    input_data JSONB,
    status VARCHAR(20) NOT NULL,
    priority INTEGER DEFAULT 5,
    progress INTEGER DEFAULT 0,
    retries INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS package_executions (
    id VARCHAR(64) PRIMARY KEY,
    package_id VARCHAR(64) NOT NULL,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL,
    progress INTEGER DEFAULT 0,
    context_data JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS package_steps (
    id VARCHAR(64) PRIMARY KEY,
    execution_id VARCHAR(64) REFERENCES package_executions(id) ON DELETE CASCADE,
    step_name VARCHAR(255) NOT NULL,
    step_type VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL,
    progress INTEGER DEFAULT 0,
    inputs JSONB,
    outputs JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);


