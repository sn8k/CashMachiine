-- signals table migration v0.1.0
CREATE TABLE IF NOT EXISTS signals (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    kind TEXT,
    value NUMERIC,
    horizon TEXT,
    confidence NUMERIC,
    ts TIMESTAMPTZ
);
