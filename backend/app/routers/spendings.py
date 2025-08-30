from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date, timedelta
from typing import List
from ..database import get_db
from ..models import Spending, User
from ..schemas import SpendingCreate, SpendingResponse, DashboardStats
from ..auth import get_current_user

router = APIRouter(prefix="/spendings", tags=["spendings"])

@router.post("", response_model=SpendingResponse)
async def create_spending(
    spending: SpendingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[SPENDING] Create spending for user {current_user.id} ({current_user.email})")
    print(f"[SPENDING] Data: {spending.dict()}")
    
    try:
        db_spending = Spending(**spending.dict(), user_id=current_user.id)
        db.add(db_spending)
        db.commit()
        db.refresh(db_spending)
        
        print(f"[SPENDING] Created spending ID {db_spending.id} for user {current_user.id}")
        return db_spending
    except Exception as e:
        print(f"[SPENDING] Error creating spending: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create spending: {str(e)}")

@router.get("", response_model=List[SpendingResponse])
async def get_spendings(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[SPENDING] Get spendings for user {current_user.id} ({current_user.email})")
    
    spendings = db.query(Spending).filter(
        Spending.user_id == current_user.id
    ).order_by(desc(Spending.date)).offset(skip).limit(limit).all()
    
    print(f"[SPENDING] Found {len(spendings)} spendings for user {current_user.id}")
    return spendings

@router.get("/date/{spending_date}", response_model=List[SpendingResponse])
async def get_spendings_by_date(
    spending_date: date, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    spendings = db.query(Spending).filter(
        Spending.date == spending_date,
        Spending.user_id == current_user.id
    ).all()
    return spendings

@router.put("/{spending_id}", response_model=SpendingResponse)
async def update_spending(
    spending_id: int, 
    spending: SpendingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_spending = db.query(Spending).filter(
        Spending.id == spending_id,
        Spending.user_id == current_user.id
    ).first()
    if not db_spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    
    for key, value in spending.dict().items():
        setattr(db_spending, key, value)
    
    db.commit()
    db.refresh(db_spending)
    return db_spending

@router.delete("/{spending_id}")
async def delete_spending(
    spending_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_spending = db.query(Spending).filter(
        Spending.id == spending_id,
        Spending.user_id == current_user.id
    ).first()
    if not db_spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    
    db.delete(db_spending)
    db.commit()
    return {"message": "Spending deleted successfully"}

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get spending dashboard statistics for current user"""
    print(f"[DASHBOARD] Getting stats for user {current_user.id} ({current_user.email})")
    
    today = date.today()
    first_day_month = today.replace(day=1)
    
    # Monthly total
    monthly_total = db.query(func.sum(Spending.amount)).filter(
        Spending.date >= first_day_month,
        Spending.date <= today,
        Spending.user_id == current_user.id
    ).scalar() or 0.0
    
    # Weekly spending (last 7 days)
    seven_days_ago = today - timedelta(days=7)
    weekly_total = db.query(func.sum(Spending.amount)).filter(
        Spending.date >= seven_days_ago,
        Spending.user_id == current_user.id
    ).scalar() or 0.0
    
    # Average daily spending (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    recent_total = db.query(func.sum(Spending.amount)).filter(
        Spending.date >= thirty_days_ago,
        Spending.user_id == current_user.id
    ).scalar() or 0.0
    avg_daily = recent_total / 30 if recent_total > 0 else 0.0
    
    # Monthly transaction count
    monthly_transactions = db.query(func.count(Spending.id)).filter(
        Spending.date >= first_day_month,
        Spending.date <= today,
        Spending.user_id == current_user.id
    ).scalar() or 0
    
    # Highest single spending this month
    highest_spending = db.query(func.max(Spending.amount)).filter(
        Spending.date >= first_day_month,
        Spending.date <= today,
        Spending.user_id == current_user.id
    ).scalar() or 0.0
    
    # Top categories this month
    top_categories = db.query(
        Spending.category,
        func.sum(Spending.amount).label('total')
    ).filter(
        Spending.date >= first_day_month,
        Spending.user_id == current_user.id
    ).group_by(Spending.category).order_by(desc('total')).limit(5).all()
    
    top_categories_dict = [{"category": cat, "amount": float(total)} for cat, total in top_categories]
    
    # All categories distribution
    all_categories = db.query(
        Spending.category,
        func.sum(Spending.amount).label('total')
    ).filter(
        Spending.date >= first_day_month,
        Spending.user_id == current_user.id
    ).group_by(Spending.category).order_by(desc('total')).all()
    
    category_distribution = [{"category": cat, "amount": float(total)} for cat, total in all_categories]
    
    # Weekly trend (last 7 days)
    weekly_trend = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_total = db.query(func.sum(Spending.amount)).filter(
            Spending.date == day,
            Spending.user_id == current_user.id
        ).scalar() or 0.0
        weekly_trend.append({
            "date": day.strftime("%m/%d"),
            "amount": float(day_total)
        })
    weekly_trend.reverse()  # Show oldest to newest
    
    # Recent spendings
    recent_spendings = db.query(Spending).filter(
        Spending.user_id == current_user.id
    ).order_by(desc(Spending.date)).limit(5).all()
    
    return DashboardStats(
        total_spending=monthly_total,
        average_daily=avg_daily,
        weekly_spending=weekly_total,
        monthly_transactions=monthly_transactions,
        highest_single_spending=highest_spending,
        top_categories=top_categories_dict,
        recent_spendings=recent_spendings,
        weekly_trend=weekly_trend,
        category_distribution=category_distribution
    )
