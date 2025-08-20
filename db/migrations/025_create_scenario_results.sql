-- create scenario_results table v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS scenario_results (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    input JSONB,
    result JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
