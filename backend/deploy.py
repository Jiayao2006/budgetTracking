#!/usr/bin/env python3
"""
Production deployment setup with enhanced error handling
"""
import os
import sys
import traceback

# Add the current directory to Python path
sys.path.insert(0, '.')

def deploy_database():
    """Deploy database with proper error handling"""
    
    print("🔗 Starting database deployment...")
    
    try:
        # Check if DATABASE_URL is set
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            print(f"✅ DATABASE_URL is configured")
            print(f"📊 Database type: {'PostgreSQL' if 'postgresql' in database_url else 'SQLite'}")
        else:
            print("⚠️ DATABASE_URL not set, using SQLite")
        
        # Import and create tables
        print("📦 Importing database modules...")
        from app.database import create_tables, engine
        
        print("🗄️ Creating database tables...")
        create_tables()
        
        # Test database connection
        print("🧪 Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        print("✅ Database deployment completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📋 Python path:", sys.path)
        traceback.print_exc()
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Database deployment failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    deploy_database()
