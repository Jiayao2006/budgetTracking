from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from sqlalchemy.exc import ProgrammingError
from datetime import date, timedelta
from typing import List
from ..database import get_db
from ..models import Spending, User
from ..schemas import SpendingCreate, SpendingResponse, DashboardStats
from ..auth import get_current_user
from ..services.currency import currency_service

router = APIRouter(prefix="/spendings", tags=["spendings"])

def ensure_spending_columns(db: Session):
    """Runtime defensive check: ensure all required spendings columns exist.
    If missing (ProgrammingError on select), attempt to add them and silently continue.
    This is a fallback in case startup healing didn't run before traffic or migration drift.
    Covers: label, original_amount, original_currency, display_currency, exchange_rate
    """
    columns_to_check = [
        ('label', 'VARCHAR(100)', None),
        ('original_amount', 'DOUBLE PRECISION', 'amount'),  # Default to amount column
        ('original_currency', 'VARCHAR(3)', "'USD'"),
        ('display_currency', 'VARCHAR(3)', "'USD'"),
        ('exchange_rate', 'DOUBLE PRECISION', '1.0')
    ]
    
    for col_name, col_type, default_value in columns_to_check:
        try:
            # Lightweight probe for each column
            db.execute(text(f"SELECT {col_name} FROM spendings LIMIT 0"))
        except ProgrammingError as e:
            msg = str(e).lower()
            if 'column' in msg and col_name in msg:
                print(f'[SCHEMA][RUNTIME] Detected missing spendings.{col_name} column – attempting on-the-fly creation')
                try:
                    # Add the column
                    if default_value:
                        db.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type} DEFAULT {default_value}"))
                        if default_value != 'amount':  # For non-amount defaults, update existing rows
                            db.execute(text(f"UPDATE spendings SET {col_name} = {default_value} WHERE {col_name} IS NULL"))
                        else:  # For original_amount, copy from amount
                            db.execute(text(f"UPDATE spendings SET {col_name} = amount WHERE {col_name} IS NULL"))
                    else:
                        db.execute(text(f"ALTER TABLE spendings ADD COLUMN {col_name} {col_type}"))
                    
                    db.commit()
                    print(f'[SCHEMA][RUNTIME] spendings.{col_name} column created successfully')
                except Exception as inner:
                    # Another concurrent request might have created it; ignore duplicate errors
                    print(f"[SCHEMA][RUNTIME] Could not create {col_name} column (may already exist): {inner}")
                    db.rollback()
            else:
                # Different ProgrammingError; re-raise
                raise

@router.post("", response_model=SpendingResponse)
async def create_spending(
    spending: SpendingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[SPENDING] Create spending for user {current_user.id} ({current_user.email})")
    print(f"[SPENDING] Data: {spending.dict()}")
    
    # Ensure required columns exist
    ensure_spending_columns(db)
    
    try:
        # Get user's preferred currency
        display_currency = current_user.preferred_currency
        original_currency = spending.original_currency.upper()
        original_amount = spending.amount
        
        # Convert amount to user's preferred currency if different
        if original_currency != display_currency:
            print(f"[SPENDING] Converting {original_amount} {original_currency} to {display_currency}")
            exchange_rate = await currency_service.get_exchange_rate(original_currency, display_currency)
            
            if exchange_rate is None:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unable to get exchange rate from {original_currency} to {display_currency}"
                )
            
            converted_amount = round(original_amount * exchange_rate, 2)
            print(f"[SPENDING] Converted amount: {converted_amount} {display_currency} (rate: {exchange_rate})")
        else:
            exchange_rate = 1.0
            converted_amount = original_amount
        
        # Create spending with currency information
        db_spending = Spending(
            amount=converted_amount,  # Converted amount in display currency
            original_amount=original_amount,  # Original amount in input currency
            original_currency=original_currency,
            display_currency=display_currency,
            exchange_rate=exchange_rate,
            category=spending.category,
            location=spending.location,
            description=spending.description,
            label=spending.label,  # Add label field here
            date=spending.date,
            user_id=current_user.id
        )
        
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
    
    # Ensure required columns exist
    ensure_spending_columns(db)
    
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
    # Ensure required columns exist
    ensure_spending_columns(db)
    
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
    # Ensure required columns exist
    ensure_spending_columns(db)
    
    db_spending = db.query(Spending).filter(
        Spending.id == spending_id,
        Spending.user_id == current_user.id
    ).first()
    if not db_spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    
    print(f"[SPENDING] Update spending ID {spending_id} for user {current_user.id}")
    print(f"[SPENDING] Update data: {spending.dict()}")
    
    try:
        # Get user's preferred currency
        display_currency = current_user.preferred_currency
        original_currency = spending.original_currency.upper()
        original_amount = spending.amount
        
        # Convert amount to user's preferred currency if different
        if original_currency != display_currency:
            print(f"[SPENDING] Converting {original_amount} {original_currency} to {display_currency}")
            exchange_rate = await currency_service.get_exchange_rate(original_currency, display_currency)
            
            if exchange_rate is None:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unable to get exchange rate from {original_currency} to {display_currency}"
                )
            
            converted_amount = round(original_amount * exchange_rate, 2)
            print(f"[SPENDING] Converted amount: {converted_amount} {display_currency} (rate: {exchange_rate})")
        else:
            exchange_rate = 1.0
            converted_amount = original_amount
        
        # Update spending with currency information
        db_spending.amount = converted_amount  # Converted amount in display currency
        db_spending.original_amount = original_amount  # Original amount in input currency
        db_spending.original_currency = original_currency
        db_spending.display_currency = display_currency
        db_spending.exchange_rate = exchange_rate
        db_spending.category = spending.category
        db_spending.location = spending.location
        db_spending.description = spending.description
        db_spending.label = spending.label
        db_spending.date = spending.date
        
        db.commit()
        db.refresh(db_spending)
        
        print(f"[SPENDING] Updated spending ID {spending_id} for user {current_user.id}")
        return db_spending
    except Exception as e:
        print(f"[SPENDING] Error updating spending: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update spending: {str(e)}")

@router.delete("/{spending_id}")
async def delete_spending(
    spending_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure required columns exist
    ensure_spending_columns(db)
    
    db_spending = db.query(Spending).filter(
        Spending.id == spending_id,
        Spending.user_id == current_user.id
    ).first()
    if not db_spending:
        raise HTTPException(status_code=404, detail="Spending not found")
    
    db.delete(db_spending)
    db.commit()
    return {"message": "Spending deleted successfully"}

@router.post("/convert-currency/{target_currency}")
async def convert_all_spendings_currency(
    target_currency: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Convert all user's spendings to a new display currency"""
    # Ensure required columns exist
    ensure_spending_columns(db)
    
    target_currency = target_currency.upper()
    
    # Update user's preferred currency
    current_user.preferred_currency = target_currency
    
    # Get all user's spendings
    spendings = db.query(Spending).filter(Spending.user_id == current_user.id).all()
    
    converted_count = 0
    for spending in spendings:
        if spending.display_currency != target_currency:
            # Convert from original currency to new target currency
            exchange_rate = await currency_service.get_exchange_rate(
                spending.original_currency, 
                target_currency
            )
            
            if exchange_rate is not None:
                spending.amount = round(spending.original_amount * exchange_rate, 2)
                spending.display_currency = target_currency
                spending.exchange_rate = exchange_rate
                converted_count += 1
    
    db.commit()
    
    return {
        "message": f"Converted {converted_count} spendings to {target_currency}",
        "target_currency": target_currency,
        "converted_count": converted_count
    }

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get spending dashboard statistics for current user"""
    print(f"[DASHBOARD] Getting stats for user {current_user.id} ({current_user.email})")
    
    # Ensure required columns exist
    ensure_spending_columns(db)
    
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
