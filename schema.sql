-- To'liq PostgreSQL sxemasi (ORM hozircha faqat intersections, incidents, agent_decisions ni ishlatadi)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin','operator','viewer')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE intersections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    lanes_count INT DEFAULT 4,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE road_segments (
    id SERIAL PRIMARY KEY,
    from_intersection INT NOT NULL REFERENCES intersections(id),
    to_intersection INT NOT NULL REFERENCES intersections(id),
    length_m NUMERIC(8,2) NOT NULL,
    speed_limit_kmh INT DEFAULT 60,
    lanes INT DEFAULT 2
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    intersection_id INT NOT NULL REFERENCES intersections(id) ON DELETE CASCADE,
    sensor_type VARCHAR(30) NOT NULL,
    direction VARCHAR(10) NOT NULL,
    status VARCHAR(20) DEFAULT 'online',
    installed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE traffic_signals (
    id SERIAL PRIMARY KEY,
    intersection_id INT NOT NULL REFERENCES intersections(id) ON DELETE CASCADE,
    controller_code VARCHAR(50) UNIQUE NOT NULL,
    current_phase INT,
    mode VARCHAR(20) DEFAULT 'adaptive'
);

CREATE TABLE signal_phases (
    id SERIAL PRIMARY KEY,
    signal_id INT NOT NULL REFERENCES traffic_signals(id) ON DELETE CASCADE,
    phase_no INT NOT NULL,
    green_seconds INT NOT NULL CHECK (green_seconds BETWEEN 5 AND 120),
    yellow_seconds INT DEFAULT 3,
    red_seconds INT NOT NULL,
    UNIQUE (signal_id, phase_no)
);

CREATE TABLE traffic_observations (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INT NOT NULL REFERENCES sensors(id),
    observed_at TIMESTAMPTZ NOT NULL,
    vehicle_count INT NOT NULL,
    avg_speed_kmh NUMERIC(5,2),
    queue_length_m NUMERIC(7,2),
    occupancy_pct NUMERIC(5,2)
);
CREATE INDEX idx_obs_sensor_time ON traffic_observations (sensor_id, observed_at DESC);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    intersection_id INT NOT NULL REFERENCES intersections(id),
    incident_type VARCHAR(40) NOT NULL,
    severity SMALLINT CHECK (severity BETWEEN 1 AND 5),
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    description TEXT
);

CREATE TABLE predictions (
    id BIGSERIAL PRIMARY KEY,
    intersection_id INT NOT NULL REFERENCES intersections(id),
    target_time TIMESTAMPTZ NOT NULL,
    predicted_count INT NOT NULL,
    confidence NUMERIC(4,3),
    model_version VARCHAR(30),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE signal_plans (
    id SERIAL PRIMARY KEY,
    signal_id INT NOT NULL REFERENCES traffic_signals(id),
    plan_json JSONB NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'proposed',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    applied_at TIMESTAMPTZ
);

CREATE TABLE emergency_events (
    id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(30) NOT NULL,
    route_json JSONB NOT NULL,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    eta_seconds INT
);

CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) UNIQUE NOT NULL,
    agent_type VARCHAR(40) NOT NULL,
    version VARCHAR(20),
    is_enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE agent_decisions (
    id BIGSERIAL PRIMARY KEY,
    agent_id INT REFERENCES agents(id),
    intersection_id INT REFERENCES intersections(id),
    input_json JSONB,
    decision_json JSONB NOT NULL,
    reasoning TEXT,
    latency_ms INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES incidents(id),
    user_id UUID REFERENCES users(id),
    channel VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(80) NOT NULL,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
