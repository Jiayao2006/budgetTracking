"""
Script to create the default admin user
Run this after setting up the database
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Base
from app.auth import get_password_hash

def create_admin_user():
    """Create default admin user"""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@budgettracker.com").first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@budgettracker.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),  # Change this password!
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
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
