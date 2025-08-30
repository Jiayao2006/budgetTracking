"""
Thorough authentication diagnostic script 
- Tests and fixes admin login
- Verifies JWT secret
- Dumps auth details for debugging
"""
import os
import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.database import SessionLocal, engine, DATABASE_URL
from app.models import User, Base
from app.auth import get_password_hash, verify_password, SECRET_KEY

def diagnose_auth():
    """Diagnose and fix authentication issues"""
    # Print environment info
    print("🔍 Authentication Diagnostic Tool")
    print("-" * 40)
    print(f"Database URL: {DATABASE_URL}")
    print(f"Database type: {'PostgreSQL' if 'postgresql' in DATABASE_URL else 'SQLite'}")
    
    # Check JWT secret
    jwt_secret = os.getenv("JWT_SECRET_KEY", None)
    print(f"JWT_SECRET_KEY set: {'✅ Yes' if jwt_secret else '❌ No'}")
    if not jwt_secret:
        print("⚠️ Warning: JWT_SECRET_KEY environment variable not set")
        print(f"Using fallback: {SECRET_KEY[:5]}...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # First list all tables
        inspector = inspect(engine)
        print("\n📋 Database tables:")
        for table_name in inspector.get_table_names():
            print(f"  - {table_name}")
        
        # Check if users table exists and has records
        try:
            user_count = db.query(User).count()
            print(f"\n👥 User count: {user_count}")
        except Exception as e:
            print(f"❌ Error counting users: {e}")
            
        # Find and fix admin user
        admin_email = "admin@budgettracker.com"
        admin_password = "admin123"
        
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if existing_admin:
            print(f"\n👑 Admin user found:")
            print(f"  ID: {existing_admin.id}")
            print(f"  Email: {existing_admin.email}")
            print(f"  Name: {existing_admin.full_name}")
            print(f"  Admin: {'✅' if existing_admin.is_admin else '❌'}")
            print(f"  Active: {'✅' if existing_admin.is_active else '❌'}")
            
            # Test current password
            print("\n🔑 Testing admin password...")
            test_pwd = verify_password("admin123", existing_admin.hashed_password)
            print(f"Password 'admin123' valid: {'✅' if test_pwd else '❌'}")
            
            if not test_pwd:
                # Fix admin password
                print("🔧 Resetting admin password...")
                existing_admin.hashed_password = get_password_hash(admin_password)
                existing_admin.is_admin = True  # Ensure admin flag is set
                existing_admin.is_active = True  # Ensure account is active
                db.commit()
                print("✅ Admin password reset to: admin123")
                
                # Verify password change
                db.refresh(existing_admin)
                new_test = verify_password("admin123", existing_admin.hashed_password)
                print(f"New password verification: {'✅ Success' if new_test else '❌ Failed'}")
        else:
            print("\n👑 Admin user not found, creating...")
            # Create admin user
            admin_user = User(
                email=admin_email,
                full_name="System Administrator",
                hashed_password=get_password_hash(admin_password),
                is_admin=True,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print("✅ Admin user created successfully!")
            print(f"  ID: {admin_user.id}")
        
        # List all users for verification
        print("\n📊 All users in database:")
        all_users = db.query(User).all()
        for user in all_users:
            print(f"  - {user.email} (Admin: {'✅' if user.is_admin else '❌'}, Active: {'✅' if user.is_active else '❌'})")
        
        print("\n✅ Authentication diagnostic complete!")
        print("📧 Admin email: admin@budgettracker.com")
        print("🔑 Admin password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error during diagnostics: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Add backend directory to path if script is run from project root
    if os.path.exists("backend") and not os.path.exists("app"):
        os.chdir("backend")
        sys.path.insert(0, ".")
    
    diagnose_auth()
