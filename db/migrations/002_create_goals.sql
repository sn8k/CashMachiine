-- goals table migration v0.1.0
CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name TEXT NOT NULL,
    start_capital NUMERIC,
    target_amount NUMERIC,
    deadline DATE,
    feasibility_score NUMERIC,
    risk_bounds JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
