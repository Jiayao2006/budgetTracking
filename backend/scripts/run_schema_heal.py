"""Manual trigger for schema self-heal on Render (PostgreSQL).
Run inside the backend working directory:
    python scripts/run_schema_heal.py
It will attempt to add missing columns: spendings.original_amount, spendings.label, users.preferred_currency.
Safe to run multiple times.
"""
import os, sys, pathlib

# Ensure backend root on path
backend_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_root))

from app.database import verify_and_heal_schema, engine, DATABASE_URL

print(f"[SCHEMA][MANUAL] Using DATABASE_URL={DATABASE_URL}")
verify_and_heal_schema()

# Show resulting columns for quick confirmation
from sqlalchemy import text
try:
    with engine.connect() as conn:
        spend_cols = [r[0] for r in conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='spendings' ORDER BY column_name"))]
        user_cols = [r[0] for r in conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY column_name"))]
        print('[SCHEMA][MANUAL] spendings columns:', spend_cols)
        print('[SCHEMA][MANUAL] users columns:', user_cols)
        missing = []
        if 'original_amount' not in spend_cols: missing.append('spendings.original_amount')
        if 'label' not in spend_cols: missing.append('spendings.label')
        if 'preferred_currency' not in user_cols: missing.append('users.preferred_currency')
        if missing:
            print('[SCHEMA][MANUAL] Still missing:', missing)
        else:
            print('[SCHEMA][MANUAL] All target columns present.')
except Exception as e:
    print('[SCHEMA][MANUAL] Diagnostics query failed:', e)
