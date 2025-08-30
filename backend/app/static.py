import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

def setup_static_files(app: FastAPI):
    """Setup static file serving for frontend"""
    
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    
    if os.path.exists(static_dir):
        print(f"✅ Static directory found: {static_dir}")
        
        # Serve static files (CSS, JS, images)
        app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")
        
        # Serve React app for all other routes (except API)
        @app.get("/{full_path:path}")
        async def serve_react_app(full_path: str):
            # Don't serve React app for API routes
            if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc"):
                return {"error": "Endpoint not found"}
            
            # Serve index.html for all non-API routes
            index_file = os.path.join(static_dir, "index.html")
            if os.path.exists(index_file):
                return FileResponse(index_file)
            else:
                return {"error": "Frontend not built"}
    else:
        print(f"⚠️ Static directory not found: {static_dir}")
        
        @app.get("/")
        async def fallback_root():
            return {
                "message": "Budget Tracker API is running",
                "status": "Frontend not built yet",
                "api_docs": "/docs"
            }
