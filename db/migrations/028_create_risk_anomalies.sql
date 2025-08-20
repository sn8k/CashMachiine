-- 028_create_risk_anomalies.sql v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS risk_anomalies (
    id SERIAL PRIMARY KEY,
    metric_date DATE NOT NULL,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id),
    metric TEXT NOT NULL,
    value NUMERIC NOT NULL,
    score NUMERIC NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
