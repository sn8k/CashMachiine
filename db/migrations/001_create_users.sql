-- users table migration v0.1.0
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    tz TEXT NOT NULL,
    kyc_level TEXT,
    risk_profile TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
