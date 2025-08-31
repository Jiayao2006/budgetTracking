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
        
        print("🗄️ Running database migrations...")
        try:
            # Try to run alembic migrations first
            import subprocess
            import alembic.config
            from alembic import command
            
            # Create alembic configuration
            alembic_cfg = alembic.config.Config("alembic.ini")
            
            # Override database URL if set in environment
            if database_url:
                alembic_cfg.set_main_option("sqlalchemy.url", database_url)
            
            print("📊 Running alembic upgrade head...")
            command.upgrade(alembic_cfg, "head")
            print("✅ Database migrations completed!")
            
        except Exception as migration_error:
            print(f"⚠️ Migration failed, falling back to create_tables: {migration_error}")
            print("🗄️ Creating database tables...")
            create_tables()
        
        # Ensure all required columns exist
        print("🔍 Verifying database schema...")
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                # Check if preferred_currency column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name = 'preferred_currency'
                """))
                
                if not result.fetchone():
                    print("⚠️ preferred_currency column missing, adding manually...")
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD'
                    """))
                    conn.commit()
                    print("✅ Added preferred_currency column manually")
                else:
                    print("✅ preferred_currency column exists")
                    
        except Exception as schema_error:
            print(f"⚠️ Schema verification failed: {schema_error}")
            # Continue anyway as this might be SQLite
        
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
