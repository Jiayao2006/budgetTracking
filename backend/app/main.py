from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, spendings, auth, admin
from .database import create_tables

app = FastAPI(title="Budget Tracking API", version="0.1.0")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api"):
        print(f"--> Incoming {request.method} {path}")
    response = await call_next(request)
    if path.startswith("/api"):
        print(f"<-- {response.status_code} {request.method} {path}")
    return response

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173", 
        "http://localhost:5174", "http://127.0.0.1:5174", 
        "http://localhost:5175", "http://127.0.0.1:5175",
        "http://localhost:5176", "http://127.0.0.1:5176"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(spendings.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Budget Tracking API"}
