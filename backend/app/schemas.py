from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    preferred_currency: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    preferred_currency: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Spending Schemas
class SpendingCreate(BaseModel):
    amount: float
    original_currency: str = "USD"  # Currency of the input amount
    category: str
    location: str
    description: Optional[str] = None
    date: date

class SpendingResponse(BaseModel):
    id: int
    amount: float  # Converted amount in display currency
    original_amount: float  # Original amount in input currency
    original_currency: str
    display_currency: str
    exchange_rate: float
    category: str
    location: str
    description: Optional[str]
    date: date
    user_id: int
    
    class Config:
        from_attributes = True

# Dashboard and Admin Schemas
class DashboardStats(BaseModel):
    total_spending: float
    average_daily: float
    top_categories: list[dict]
    recent_spendings: list[SpendingResponse]
    weekly_spending: float
    monthly_transactions: int
    highest_single_spending: float
    weekly_trend: list[dict]  # Last 7 days spending data
    category_distribution: list[dict]  # All categories with totals

class AdminDashboard(BaseModel):
    total_users: int
    total_admins: int
    active_users: int
    inactive_users: int
    recent_users: list[UserResponse]

# Currency Schemas
class CurrencyInfo(BaseModel):
    code: str
    name: str
    symbol: str

class ExchangeRate(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    date: str

class CurrencyConversion(BaseModel):
    original_amount: float
    original_currency: str
    target_currency: str
    converted_amount: float
    exchange_rate: float
