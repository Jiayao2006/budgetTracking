"""
Script to force create or verify the default admin user
Run this directly against the production database
"""
import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, DATABASE_URL
from app.models import User, Base
from app.auth import get_password_hash

def force_admin_user():
    """Create default admin user or reset password if it exists"""
    # Print environment info
    print(f"Database URL: {DATABASE_URL}")
    print(f"Database type: {'PostgreSQL' if 'postgresql' in DATABASE_URL else 'SQLite'}")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if admin already exists
        admin_email = "admin@budgettracker.com"
        admin_password = "admin123"
        
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if existing_admin:
            print(f"Admin user exists with ID: {existing_admin.id}")
            # Update password
            existing_admin.hashed_password = get_password_hash(admin_password)
            existing_admin.is_admin = True  # Ensure admin flag is set
            existing_admin.is_active = True  # Ensure account is active
            db.commit()
            print("✅ Admin password reset to: admin123")
        else:
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
        
        print("📧 Email: admin@budgettracker.com")
        print("🔑 Password: admin123")
        print("⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error managing admin user: {e}")
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
    
    force_admin_user()
