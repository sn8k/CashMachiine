-- positions table migration v0.1.0
CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id),
    symbol TEXT NOT NULL,
    venue TEXT,
    qty NUMERIC,
    avg_price NUMERIC,
    leverage NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
