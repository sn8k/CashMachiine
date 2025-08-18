-- accounts table migration v0.1.0
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    broker TEXT NOT NULL,
    base_ccy TEXT,
    margin_allowed BOOLEAN,
    fees_model TEXT
);
