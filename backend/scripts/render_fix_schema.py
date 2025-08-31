"""
PostgreSQL Schema Fix Script optimized for Render.
Run this to ensure all required columns exist in the database.
"""
import os, sys

# Detect environment and set DATABASE_URL from Render env if needed
if not os.getenv("DATABASE_URL") and os.getenv("RENDER"):
    print("[RENDER] Running in Render environment, configuring for PostgreSQL")
else:
    print("[LOCAL] Using local DATABASE_URL configuration")

# Import necessary tools
try:
    from sqlalchemy import create_engine, text, inspect
    print("[SQL] Successfully imported SQLAlchemy")
except ImportError:
    print("[ERROR] SQLAlchemy not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sqlalchemy"])
    from sqlalchemy import create_engine, text, inspect

try:
    import psycopg2
    print("[SQL] Using psycopg2 driver")
    pg_driver = "psycopg2"
except ImportError:
    try:
        import psycopg
        print("[SQL] Using psycopg (v3) driver")
        pg_driver = "psycopg"
    except ImportError:
        print("[ERROR] No PostgreSQL driver found! Installing psycopg2...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
        import psycopg2
        pg_driver = "psycopg2"
        print("[SQL] Installed and using psycopg2 driver")

# Get the DATABASE_URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("[ERROR] DATABASE_URL not set!")
    sys.exit(1)

# Handle PostgreSQL URL format from cloud providers
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")
    print(f"[SQL] Reformatted DATABASE_URL to use postgresql:// prefix")

# Create engine with appropriate configuration
if pg_driver:
    postgresql_url = database_url.replace("postgresql://", f"postgresql+{pg_driver}://")
    print(f"[SQL] Using PostgreSQL URL with {pg_driver}: {postgresql_url}")
    engine = create_engine(postgresql_url)
else:
    print(f"[SQL] Using default PostgreSQL URL: {database_url}")
    engine = create_engine(database_url)

def fix_schema():
    """Comprehensive schema fix for PostgreSQL.
    Adds all required columns in a single function.
    """
    try:
        with engine.connect() as conn:
            # Check existing structure
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            print(f"[SCHEMA] Found tables: {tables}")
            
            if 'spendings' in tables:
                spend_cols = {c['name'] for c in inspector.get_columns('spendings')}
                print(f"[SCHEMA] Spending columns: {spend_cols}")
                
                # Define all required columns with their SQL types and defaults
                required_columns = [
                    ('original_amount', 'DOUBLE PRECISION', 'amount'),  # Copy from amount
                    ('label', 'VARCHAR(100)', None),  # Nullable
                    ('original_currency', 'VARCHAR(3)', "'USD'"),
                    ('display_currency', 'VARCHAR(3)', "'USD'"),
                    ('exchange_rate', 'DOUBLE PRECISION', '1.0')
                ]
                
                for col_name, col_type, default_value in required_columns:
                    if col_name not in spend_cols:
                        print(f"[SCHEMA][FIX] Adding spendings.{col_name} column")
                        
                        if default_value == 'amount':
                            # Special case for original_amount - copy from existing amount column
                            conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}"))
                            conn.execute(text(f"UPDATE spendings SET {col_name} = amount WHERE {col_name} IS NULL"))
                            try:
                                conn.execute(text(f"ALTER TABLE spendings ALTER COLUMN {col_name} SET NOT NULL"))
                                print(f"[SCHEMA][FIX] Set {col_name} NOT NULL")
                            except Exception as e:
                                print(f"[SCHEMA][WARN] Could not set NOT NULL on {col_name}: {e}")
                        elif default_value:
                            # Other columns with default values
                            conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type} DEFAULT {default_value}"))
                            conn.execute(text(f"UPDATE spendings SET {col_name} = {default_value} WHERE {col_name} IS NULL"))
                        else:
                            # Nullable columns (like label)
                            conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}"))
            else:
                print("[SCHEMA][ERROR] No spendings table found!")
                
            if 'users' in tables:
                user_cols = {c['name'] for c in inspector.get_columns('users')}
                print(f"[SCHEMA] User columns: {user_cols}")
                
                # Fix preferred_currency
                if 'preferred_currency' not in user_cols:
                    print("[SCHEMA][FIX] Adding users.preferred_currency column")
                    conn.execute(text("ALTER TABLE users ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD'"))
            else:
                print("[SCHEMA][ERROR] No users table found!")
                
            conn.commit()
            print("[SCHEMA][SUCCESS] All fixes committed successfully")
            
            # Validate the schema
            try:
                inspector = inspect(engine)
                spend_cols = {c['name'] for c in inspector.get_columns('spendings')}
                user_cols = {c['name'] for c in inspector.get_columns('users')}
                
                # Check for required columns
                required_spending = ['original_amount', 'label', 'original_currency', 'display_currency', 'exchange_rate']
                missing = []
                
                if 'spendings' in tables:
                    for col in required_spending:
                        if col not in spend_cols:
                            missing.append(f'spendings.{col}')
                            
                if 'users' in tables:    
                    if 'preferred_currency' not in user_cols:
                        missing.append('users.preferred_currency')
                
                if missing:
                    print(f"[SCHEMA][VALIDATION] Still missing columns: {missing}")
                else:
                    print("[SCHEMA][VALIDATION] All required columns exist!")
            except Exception as e:
                print(f"[SCHEMA][VALIDATION] Error during validation: {e}")
                
    except Exception as e:
        print(f"[SCHEMA][ERROR] Failed during schema fix: {e}")

# Run the fix
print("[RENDER-FIX] Starting schema repair...")
fix_schema()
print("[RENDER-FIX] Schema repair complete")
