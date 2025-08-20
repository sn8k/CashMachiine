-- risk_anomalies table migration v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS risk_anomalies (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    portfolio_id INTEGER REFERENCES portfolios(id),
    metric TEXT NOT NULL,
    value NUMERIC NOT NULL,
    score NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);
