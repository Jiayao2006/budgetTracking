-- Manual SQL script to add missing preferred_currency column
-- Run this if alembic migration fails

-- Add preferred_currency column to users table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'users' 
        AND column_name = 'preferred_currency'
    ) THEN
        ALTER TABLE users ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD';
        RAISE NOTICE 'Added preferred_currency column to users table';
    ELSE
        RAISE NOTICE 'preferred_currency column already exists';
    END IF;
END $$;

-- Verify the column was added
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'users' 
AND column_name = 'preferred_currency';
