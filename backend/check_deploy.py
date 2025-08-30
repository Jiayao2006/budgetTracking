#!/usr/bin/env python3
"""
Render deployment check script
"""
import os
import sys

def check_environment():
    print("🔍 Checking Render environment...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check environment variables
    print(f"PORT: {os.getenv('PORT', 'Not set')}")
    print(f"DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
    
    # Check if we can import our app
    try:
        sys.path.append('.')
        from app.main import app
        print("✅ App import successful")
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False
    
    # Check database connection
    try:
        from app.database import engine
        print("✅ Database engine created")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if check_environment():
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed!")
        sys.exit(1)
