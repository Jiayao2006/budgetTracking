from pydantic import BaseModel
from datetime import date
from typing import Optional

class SpendingCreate(BaseModel):
    amount: float
    category: str
    location: str
    description: Optional[str] = None
    date: date

class SpendingResponse(BaseModel):
    id: int
    amount: float
    category: str
    location: str
    description: Optional[str]
    date: date
    
    class Config:
        from_attributes = True

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
