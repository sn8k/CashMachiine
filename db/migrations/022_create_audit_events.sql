-- 022_create_audit_events.sql v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS audit_events (
    id SERIAL PRIMARY KEY,
    event VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    tenant_id INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
