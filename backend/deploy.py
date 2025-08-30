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
        from sqlalchemy import text
        from app.database import SessionLocal
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create default admin user
        print("👑 Creating admin user...")
        db = SessionLocal()
        try:
            from app.models import User
            from app.auth import get_password_hash
            
            # Check if admin already exists
            existing_admin = db.query(User).filter(User.email == "admin@budgettracker.com").first()
            if existing_admin:
                print("✅ Admin user already exists!")
            else:
                # Create admin user
                admin_user = User(
                    email="admin@budgettracker.com",
                    full_name="System Administrator", 
                    hashed_password=get_password_hash("admin123"),
                    is_admin=True,
                    is_active=True
                )
                
                db.add(admin_user)
                db.commit()
                print("✅ Admin user created: admin@budgettracker.com / admin123")
        except Exception as admin_error:
            print(f"⚠️ Admin user creation failed: {admin_error}")
            db.rollback()
        finally:
            db.close()
        
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
