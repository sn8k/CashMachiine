-- 026_create_alerts.sql v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    notification_id INTEGER NOT NULL REFERENCES notifications(id),
    created_at TIMESTAMPTZ DEFAULT now()
);
