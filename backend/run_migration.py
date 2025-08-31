#!/usr/bin/env python3
"""
Script to run database migrations in production
"""
import os
import subprocess
import sys

def run_migration():
    """Run alembic migration to upgrade database"""
    try:
        print("Running database migration...")
        
        # Ensure we're in the backend directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_dir)
        
        # Run alembic upgrade
        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migration completed successfully!")
            print(result.stdout)
        else:
            print("❌ Migration failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False
    
    return True

def check_database_connection():
    """Check if database is accessible"""
    try:
        from app.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Database Migration Script ===")
    
    # Check environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)
    
    print(f"Database URL: {database_url[:20]}...")
    
    # Check connection
    if not check_database_connection():
        sys.exit(1)
    
    # Run migration
    if run_migration():
        print("🎉 Migration process completed successfully!")
    else:
        print("💥 Migration process failed!")
        sys.exit(1)
