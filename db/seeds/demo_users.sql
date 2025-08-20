-- demo_users.sql v0.1.0 (2025-02-14)
CREATE TABLE IF NOT EXISTS demo_users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO demo_users (email) VALUES ('demo@example.com') ON CONFLICT DO NOTHING;
