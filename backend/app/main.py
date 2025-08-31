import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, spendings, auth, admin, currency, users, labels
from .database import create_tables, verify_and_heal_schema, engine
from sqlalchemy import text
from .static import setup_static_files

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    create_tables()
    verify_and_heal_schema()
    yield
    # (No special shutdown needed)

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

# Always allow deployed production domain (Render) if provided
default_prod_domain = os.getenv("PROD_DOMAIN", "https://budget-tracker-fullstack.onrender.com").strip()
if default_prod_domain and default_prod_domain not in allowed_origins:
    allowed_origins.append(default_prod_domain)

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
app.include_router(labels.router)

# Lightweight diagnostics (admin use; no sensitive data exposed)
@app.get("/api/diagnostics/schema")
async def schema_diagnostics():
    try:
        with engine.connect() as conn:
            spend_cols = []
            user_cols = []
            try:
                res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='spendings' ORDER BY column_name"))
                spend_cols = [r[0] for r in res.fetchall()]
            except Exception:
                pass
            try:
                res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' ORDER BY column_name"))
                user_cols = [r[0] for r in res.fetchall()]
            except Exception:
                pass
            
            # Check for all required columns
            required_spending_cols = ['original_amount', 'label', 'original_currency', 'display_currency', 'exchange_rate']
            missing_spending = [col for col in required_spending_cols if col not in spend_cols]
            
            return {
                "spendings_columns": spend_cols,
                "users_columns": user_cols,
                "needs_original_amount": 'original_amount' not in spend_cols,
                "needs_label": 'label' not in spend_cols,
                "needs_original_currency": 'original_currency' not in spend_cols,
                "needs_display_currency": 'display_currency' not in spend_cols,
                "needs_exchange_rate": 'exchange_rate' not in spend_cols,
                "needs_preferred_currency": 'preferred_currency' not in user_cols,
                "missing_spending_columns": missing_spending,
                "all_required_present": len(missing_spending) == 0 and 'preferred_currency' in user_cols
            }
    except Exception as e:
        return {"error": str(e)}

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
