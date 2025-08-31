#!/bin/bash
# Emergency database fix script for Render shell
# Run this in Render shell: bash emergency_db_fix.sh

echo "🚨 EMERGENCY DATABASE FIX"
echo "========================="

# Navigate to the correct directory
cd /opt/render/project/src/backend

# Run the Python fix script
echo "Running database column fix..."
python fix_spending_columns.py

echo "Done. Check if the application is now working."
