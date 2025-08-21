-- 000_demo_users_2025-08-22.sql v0.1.1 (2025-08-22)
CREATE TABLE IF NOT EXISTS demo_users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO demo_users (email) VALUES ('demo@example.com') ON CONFLICT DO NOTHING;
