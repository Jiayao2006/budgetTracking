#!/usr/bin/env python3
"""
Database migration script for PostgreSQL setup
Run this when you have a PostgreSQL DATABASE_URL set up
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Add the app directory to the path
sys.path.append('.')

from app.models import Base, User, Spending
from app.database import DATABASE_URL, engine

def setup_postgresql_database():
    """Initialize PostgreSQL database with proper schema and admin user"""
    
    print("🗄️  Setting up PostgreSQL database...")
    print(f"Database URL: {str(engine.url).replace(str(engine.url).split('@')[0].split('://')[-1], '***')}")
    
    try:
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@budgettracker.com").first()
        
        if not admin_user:
            print("👤 Creating admin user...")
            # Create admin user
            admin_user = User(
                email="admin@budgettracker.com",
                full_name="Admin User",
                hashed_password=pwd_context.hash("admin123"),
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Admin user created with ID: {admin_user.id}")
        else:
            print(f"✅ Admin user already exists with ID: {admin_user.id}")
        
        print("🎉 PostgreSQL database setup completed successfully!")
        
        # Verify the setup
        print("\n🔍 Verifying database setup...")
        user_count = db.query(User).count()
        spending_count = db.query(Spending).count()
        print(f"📊 Users: {user_count}, Spendings: {spending_count}")
        
        print("\n📋 Admin login credentials:")
        print("   Email: admin@budgettracker.com")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        raise
    finally:
        db.close()

def check_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            if DATABASE_URL.startswith("postgresql"):
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Connected to PostgreSQL: {version.split()[0]} {version.split()[1]}")
            else:
                print("✅ Connected to SQLite database")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Database Migration Script")
    print("=" * 50)
    
    # Check connection first
    if not check_database_connection():
        sys.exit(1)
    
    # Determine database type
    if DATABASE_URL.startswith("postgresql"):
        print("🐘 PostgreSQL database detected")
        setup_postgresql_database()
    else:
        print("📁 SQLite database detected")
        print("💡 To use PostgreSQL, set the DATABASE_URL environment variable")
        print("   Example: DATABASE_URL=postgresql://user:pass@host:5432/dbname")
        
        # Still create tables for SQLite
        print("📋 Creating SQLite tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ SQLite setup completed")
