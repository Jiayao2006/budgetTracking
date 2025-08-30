#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""
import os
import sys
import uvicorn

def start_server():
    """Start the FastAPI server with proper configuration"""
    
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Budget Tracker API...")
    print(f"📍 Port: {port}")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🗄️ Database: {'PostgreSQL' if os.getenv('DATABASE_URL') else 'SQLite'}")
    
    # Add current directory to Python path
    sys.path.insert(0, '.')
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=False
        )
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
