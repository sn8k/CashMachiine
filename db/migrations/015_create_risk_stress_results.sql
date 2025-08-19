-- risk_stress_results table migration v0.1.0
CREATE TABLE IF NOT EXISTS risk_stress_results (
    id SERIAL PRIMARY KEY,
    scenario TEXT NOT NULL,
    metric JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
