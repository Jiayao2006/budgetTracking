import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, create_tables
from app.models import User, Base
from app.auth import get_password_hash

# Create all tables
create_tables()
print("✅ Tables created!")

# Create admin user
db = SessionLocal()
try:
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == "admin@budgettracker.com").first()
    if existing_admin:
        print("⚠️ Admin user already exists!")
        print(f"📧 Email: {existing_admin.email}")
        print(f"👤 Name: {existing_admin.full_name}")
        print(f"🔧 Admin: {existing_admin.is_admin}")
        print(f"✅ Active: {existing_admin.is_active}")
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
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print("📧 Email: admin@budgettracker.com")
        print("🔑 Password: admin123")
        print("⚠️ Please change the password after first login!")
    
    # Create a test regular user
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if not existing_user:
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print("📧 Email: test@example.com")
        print("🔑 Password: password123")
    else:
        print("⚠️ Test user already exists!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

print("\n🚀 Authentication system is ready!")
print("🌐 Frontend: http://localhost:5173")
print("🔧 Backend API: http://localhost:8000")
print("📖 API Docs: http://localhost:8000/docs")
