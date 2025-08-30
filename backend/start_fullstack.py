#!/usr/bin/env python3
"""
Full-stack production startup script
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Budget Tracker Full Stack on port {port}")
    print("📱 Frontend: Available at /")
    print("🔌 API: Available at /api/*")
    print("📖 Docs: Available at /docs")
    print(f"🗄️ Database: {'PostgreSQL' if os.getenv('DATABASE_URL') else 'SQLite'}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
