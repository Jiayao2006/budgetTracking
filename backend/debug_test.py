#!/usr/bin/env python3
"""
Simple deployment test script for debugging Render issues
"""
import os
import sys

print("🧪 RENDER DEPLOYMENT DEBUG TEST")
print("=" * 50)

print(f"🐍 Python version: {sys.version}")
print(f"📂 Current directory: {os.getcwd()}")
print(f"📋 Python path: {sys.path}")
print(f"🌐 PORT environment: {os.getenv('PORT', 'Not set')}")
print(f"🗄️ DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")

print("\n📦 Testing imports...")

try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import uvicorn
    print(f"✅ Uvicorn: Available")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
except ImportError as e:
    print(f"❌ SQLAlchemy import failed: {e}")

try:
    sys.path.insert(0, '.')
    from app.main import app
    print(f"✅ App import: Success")
except ImportError as e:
    print(f"❌ App import failed: {e}")
    
try:
    from app.database import DATABASE_URL, engine
    print(f"✅ Database config: Loaded")
    print(f"📊 Database URL type: {'PostgreSQL' if 'postgresql' in DATABASE_URL else 'SQLite'}")
except ImportError as e:
    print(f"❌ Database import failed: {e}")

print("\n🎯 Test completed!")
print("=" * 50)
