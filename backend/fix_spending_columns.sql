-- Fix script for missing columns in spendings table
ALTER TABLE spendings ADD COLUMN IF NOT EXISTS original_amount FLOAT;
ALTER TABLE spendings ADD COLUMN IF NOT EXISTS label VARCHAR(100);

-- Update original_amount to match amount for existing records
UPDATE spendings SET original_amount = amount WHERE original_amount IS NULL;

-- Make original_amount not nullable after setting values
ALTER TABLE spendings ALTER COLUMN original_amount SET NOT NULL;
