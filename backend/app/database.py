import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from .models import Base

# Support both development (SQLite) and production (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Clean up empty or whitespace-only DATABASE_URL
if not DATABASE_URL or DATABASE_URL.strip() == "":
    DATABASE_URL = "sqlite:///./budget.db"

# Handle PostgreSQL URL format from cloud providers
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Try to determine which PostgreSQL driver is available
pg_driver = "psycopg"  # Default to psycopg (v3)
try:
    import psycopg
    print("Using psycopg v3 driver")
except ImportError:
    try:
        import psycopg2
        pg_driver = "psycopg2"
        print("Using psycopg2 driver")
    except ImportError:
        print("WARNING: No PostgreSQL driver found. Will attempt with SQLAlchemy defaults.")
        pg_driver = None

# Create engine with appropriate configuration
if DATABASE_URL.startswith("postgresql://"):
    # PostgreSQL configuration with dynamic driver selection
    if pg_driver:
        # Use specific driver if available
        postgresql_url = DATABASE_URL.replace("postgresql://", f"postgresql+{pg_driver}://")
        print(f"Using PostgreSQL URL with {pg_driver}: {postgresql_url}")
        engine = create_engine(postgresql_url)
    else:
        # Let SQLAlchemy choose driver
        print(f"Using default PostgreSQL URL: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
else:
    # SQLite configuration (for local development)
    print(f"Using SQLite URL: {DATABASE_URL}")
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def verify_and_heal_schema():
    """Ensure critical columns exist (idempotent). Used at startup in production.
    Adds missing columns for spendings (original_amount, label, original_currency, display_currency, exchange_rate)
    and users (preferred_currency).
    Safe to run repeatedly. Logs actions; ignores errors when columns already exist.
    """
    if not DATABASE_URL.startswith("postgresql"):
        # Skip for SQLite dev; tests/migrations cover local.
        return
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if 'spendings' in tables:
                cols = {c['name'] for c in inspector.get_columns('spendings')}
                
                # Define all required columns with their types and defaults
                required_columns = [
                    ('original_amount', 'DOUBLE PRECISION', 'amount'),
                    ('label', 'VARCHAR(100)', None),
                    ('original_currency', 'VARCHAR(3)', "'USD'"),
                    ('display_currency', 'VARCHAR(3)', "'USD'"),
                    ('exchange_rate', 'DOUBLE PRECISION', '1.0')
                ]
                
                for col_name, col_type, default_value in required_columns:
                    if col_name not in cols:
                        print(f'[SCHEMA] Adding spendings.{col_name}')
                        if default_value:
                            if default_value == 'amount':
                                # Special case for original_amount - copy from amount
                                conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}"))
                                conn.execute(text(f"UPDATE spendings SET {col_name} = amount WHERE {col_name} IS NULL"))
                                try:
                                    conn.execute(text(f"ALTER TABLE spendings ALTER COLUMN {col_name} SET NOT NULL"))
                                except Exception as e:
                                    print(f"[SCHEMA] Could not set NOT NULL on {col_name}: {e}")
                            else:
                                # Other columns with default values
                                conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type} DEFAULT {default_value}"))
                                conn.execute(text(f"UPDATE spendings SET {col_name} = {default_value} WHERE {col_name} IS NULL"))
                        else:
                            # Nullable columns
                            conn.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}"))
                            
            if 'users' in tables:
                ucols = {c['name'] for c in inspector.get_columns('users')}
                if 'preferred_currency' not in ucols:
                    print('[SCHEMA] Adding users.preferred_currency')
                    conn.execute(text("ALTER TABLE users ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD'"))
                    
            conn.commit()
    except Exception as e:
        # Log but do not crash app startup
        print(f"[SCHEMA] Verification/heal failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
