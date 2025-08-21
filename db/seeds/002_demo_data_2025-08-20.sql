-- 002_demo_data_2025-08-20.sql v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS demo_accounts (
    id SERIAL PRIMARY KEY,
    user_email TEXT NOT NULL,
    balance NUMERIC DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO demo_accounts (user_email, balance)
VALUES ('demo@example.com', 1000)
ON CONFLICT DO NOTHING;
