#!/usr/bin/env bash
# Fix production database issues

echo "🚨 EMERGENCY DATABASE FIX SCRIPT"
echo "===============================
=
This script will fix missing columns in the spendings table on your production database.
"

# Run our emergency fix script
echo "🔧 Running database fix script..."
python fix_spending_columns.py

# Run migrations to ensure all tables are up to date
echo "📊 Running migrations..."
python -m alembic upgrade head

# Test database queries
echo "🧪 Testing database queries..."
python -c "
import os
from sqlalchemy import create_engine, text
from app.database import SessionLocal, engine
from app.models import Spending, User

# Test spendings table columns
try:
    db = SessionLocal()
    user = db.query(User).first()
    if user:
        print(f'✅ Found user: {user.email}')
    else:
        print('⚠️ No users found')
    
    # Test spending label column
    try:
        db.execute(text('SELECT label FROM spendings LIMIT 1'))
        print('✅ Label column exists')
    except Exception as e:
        print(f'❌ Label column error: {e}')
    
    # Test spending original_amount column
    try:
        db.execute(text('SELECT original_amount FROM spendings LIMIT 1'))
        print('✅ Original amount column exists')
    except Exception as e:
        print(f'❌ Original amount column error: {e}')
    
    # Close session
    db.close()
    print('✅ Database test completed')
except Exception as e:
    print(f'❌ Database test error: {e}')
"

echo "
===============================
✅ FIX PROCESS COMPLETE

If everything shows successful, your application should now work correctly.
If there are still errors, please contact development support.
"
