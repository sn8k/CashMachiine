-- orders table migration v0.1.0
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    symbol TEXT NOT NULL,
    side TEXT,
    qty NUMERIC,
    type TEXT,
    limit_price NUMERIC,
    status TEXT,
    reason TEXT,
    sl NUMERIC,
    tp NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
