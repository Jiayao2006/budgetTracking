import os
from sqlalchemy import create_engine
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
