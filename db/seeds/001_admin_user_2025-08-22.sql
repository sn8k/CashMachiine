-- 001_admin_user_2025-08-22.sql v0.1.1 (2025-08-22)
INSERT INTO users (email, password, role, created_at)
VALUES ('admin@cashmachiine.local', 'admin', 'admin', NOW())
ON CONFLICT (email) DO NOTHING;
