-- add kyc_level to users v0.1.0
ALTER TABLE IF EXISTS users ADD COLUMN IF NOT EXISTS kyc_level TEXT;
