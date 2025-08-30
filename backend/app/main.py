import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, spendings, auth, admin
from .database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(title="Budget Tracking API", version="0.1.0", lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api"):
        print(f"--> Incoming {request.method} {path}")
    response = await call_next(request)
    if path.startswith("/api"):
        print(f"<-- {response.status_code} {request.method} {path}")
    return response

# Environment-based CORS configuration
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

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(spendings.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Budget Tracking API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "configured"}

# For production deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
