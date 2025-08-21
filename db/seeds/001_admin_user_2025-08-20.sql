-- 001_admin_user_2025-08-20.sql v0.1.0 (2025-08-20)
INSERT INTO users (email, password, role, created_at)
VALUES ('admin@cashmachiine.local', 'admin', 'admin', NOW())
ON CONFLICT (email) DO NOTHING;
