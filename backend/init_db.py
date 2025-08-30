#!/usr/bin/env python3
"""
Database initialization script
Creates the database with proper schema and seed data
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import date

# Add the app directory to the path
sys.path.append('.')

from app.models import Base, User, Spending
from app.database import SQLALCHEMY_DATABASE_URL

def init_database():
    """Initialize the database with proper schema and seed data"""
    
    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create password context
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Check if admin user exists
        admin_user = db.query(User).filter(User.email == "admin@budgettracker.com").first()
        
        if not admin_user:
            print("Creating admin user...")
            # Create admin user
            admin_user = User(
                email="admin@budgettracker.com",
                full_name="Admin User",
                hashed_password=pwd_context.hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Admin user created with ID: {admin_user.id}")
        else:
            print(f"Admin user already exists with ID: {admin_user.id}")
        
        # Create a test spending record
        existing_spending = db.query(Spending).filter(Spending.user_id == admin_user.id).first()
        if not existing_spending:
            print("Creating test spending record...")
            test_spending = Spending(
                amount=50.0,
                category="Food",
                location="Test Restaurant",
                description="Test spending record",
                date=date(2025, 8, 30),
                user_id=admin_user.id
            )
            db.add(test_spending)
            db.commit()
            print("Test spending record created")
        else:
            print("Test spending records already exist")
        
        print("Database initialization completed successfully!")
        
        # Simple verification
        print("\nVerifying database...")
        spending_count = db.query(Spending).count()
        user_count = db.query(User).count()
        print(f"Users: {user_count}, Spendings: {spending_count}")
        print("✅ Database initialized with proper schema and user_id column")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
