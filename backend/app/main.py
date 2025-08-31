import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, spendings, auth, admin, currency, users
from .database import create_tables
from .static import setup_static_files

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(title="Budget Tracking Full Stack", version="1.0.0", lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api"):
        print(f"--> Incoming {request.method} {path}")
    response = await call_next(request)
    if path.startswith("/api"):
        print(f"<-- {response.status_code} {request.method} {path}")
    return response

# Environment-based CORS configuration (for development)
allowed_origins = [
    "http://localhost:5173", "http://127.0.0.1:5173", 
    "http://localhost:5174", "http://127.0.0.1:5174", 
    "http://localhost:5175", "http://127.0.0.1:5175",
    "http://localhost:5176", "http://127.0.0.1:5176"
]

# Add production origins from environment variable
production_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
allowed_origins.extend([origin.strip() for origin in production_origins if origin.strip()])

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router)
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(currency.router)
app.include_router(users.router, prefix="/api")
app.include_router(spendings.router, prefix="/api")

# API health endpoints
@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy", "database": "configured", "type": "fullstack"}

@app.get("/api/")
async def api_root():
    return {
        "message": "Budget Tracker API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "type": "fullstack"
    }

# Setup static file serving for React frontend
setup_static_files(app)

# For production deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
