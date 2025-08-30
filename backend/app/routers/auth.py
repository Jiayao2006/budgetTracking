from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    print("[AUTH] /register called for", user.email)
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_admin=False,  # Regular users are not admin by default
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token for the new user
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    print("[AUTH] /register success token issued for", db_user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    email: str = Form(None),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    """Login user and return access token. Accepts JSON {email,password} or form-data."""
    body_email = None
    body_password = None
    client_host = request.client.host if request.client else "unknown"
    
    # Try to extract credentials from form or JSON
    if email and password:
        body_email, body_password = email, password
        print(f"[AUTH] Login attempt from {client_host} using form data for: {body_email}")
    else:
        try:
            data = await request.json()
            body_email = data.get("email")
            body_password = data.get("password")
            print(f"[AUTH] Login attempt from {client_host} using JSON for: {body_email}")
        except Exception as e:
            print(f"[AUTH] Failed to parse request body: {e}")
            pass
    
    if not body_email or not body_password:
        print("[AUTH] Missing email or password")
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Check if user exists
    user_exists = db.query(User).filter(User.email == body_email).first() is not None
    if not user_exists:
        print(f"[AUTH] Login failed - user not found: {body_email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not found: {body_email}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Try to authenticate
    user = authenticate_user(db, body_email, body_password)
    if not user:
        print(f"[AUTH] Login failed - invalid password for: {body_email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print(f"[AUTH] Login success for {user.email} (admin: {user.is_admin})")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/logout")
def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}
