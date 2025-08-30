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
    if email and password:
        body_email, body_password = email, password
    else:
        try:
            data = await request.json()
            body_email = data.get("email")
            body_password = data.get("password")
        except Exception:
            pass
    print("[AUTH] /login attempt for", body_email)
    if not body_email or not body_password:
        raise HTTPException(status_code=400, detail="Email and password required")
    user = authenticate_user(db, body_email, body_password)
    if not user:
        print("[AUTH] /login failed for", body_email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print("[AUTH] /login success for", user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/logout")
def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}
