-- add oauth and 2fa columns to users v0.1.0
ALTER TABLE IF EXISTS users
    ADD COLUMN IF NOT EXISTS oauth_provider TEXT,
    ADD COLUMN IF NOT EXISTS oauth_sub TEXT,
    ADD COLUMN IF NOT EXISTS totp_secret TEXT,
    ADD COLUMN IF NOT EXISTS backup_codes TEXT[];
