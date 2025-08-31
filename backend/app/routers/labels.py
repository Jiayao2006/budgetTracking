from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from sqlalchemy.exc import ProgrammingError
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..models import User, Spending
from ..schemas import LabelStats, LabelsOverview
from ..auth import get_current_user
from ..services.currency import currency_service

router = APIRouter(prefix="/api/labels", tags=["labels"])

def ensure_label_column(db: Session):
    """Runtime defensive check: ensure spendings.label column exists.
    If missing (ProgrammingError on select), attempt to add it and silently continue.
    This is a fallback in case startup healing didn't run before traffic or migration drift.
    """
    try:
        # Lightweight probe
        db.execute(text("SELECT label FROM spendings LIMIT 0"))
    except ProgrammingError as e:
        msg = str(e).lower()
        if 'column' in msg and 'label' in msg:
            print('[SCHEMA][RUNTIME] Detected missing spendings.label column – attempting on-the-fly creation')
            try:
                db.execute(text("ALTER TABLE spendings ADD COLUMN label VARCHAR(100)"))
                db.commit()
                print('[SCHEMA][RUNTIME] spendings.label column created successfully')
            except Exception as inner:
                # Another concurrent request might have created it; ignore duplicate errors
                print(f"[SCHEMA][RUNTIME] Could not create label column (may already exist): {inner}")
                db.rollback()
        else:
            # Different ProgrammingError; re-raise
            raise

@router.get("/debug", response_model=dict)
async def debug_labels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Debug endpoint to check what's in the database"""
    all_spendings = db.query(Spending).filter(Spending.user_id == current_user.id).all()
    
    # Test the query that should retrieve labels
    test_query = db.query(Spending.label).filter(
        Spending.user_id == current_user.id,
        Spending.label.isnot(None),
        Spending.label != ""
    ).distinct().all()
    
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "total_spendings": len(all_spendings),
        "test_query_results": [label[0] for label in test_query],
        "spendings_with_labels": [
            {
                "id": s.id,
                "label": s.label,
                "amount": s.amount,
                "location": s.location,
                "date": str(s.date)
            } 
            for s in all_spendings if s.label
        ],
        "all_labels": [s.label for s in all_spendings if s.label]
    }

@router.get("/list", response_model=List[str])
async def get_available_labels(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of all unique labels used by the current user"""
    ensure_label_column(db)
    labels_query = db.query(Spending.label).filter(
        Spending.user_id == current_user.id,
        Spending.label.isnot(None),
        Spending.label != ""
    ).distinct()
    
    labels = labels_query.all()
    
    # Filter out empty strings and None values
    result = [label[0] for label in labels if label[0] and label[0].strip() != ""]
    return result

@router.get("/", response_model=LabelsOverview)
async def get_labels_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overview of all labels with statistics"""
    ensure_label_column(db)
    print(f"[LABELS] Getting labels overview for user {current_user.id} ({current_user.email})")
    
    # First check if there are any spendings with labels for this user
    all_spendings = db.query(Spending).filter(
        Spending.user_id == current_user.id,
        Spending.label.isnot(None),
        func.trim(Spending.label) != ""
    ).all()
    
    print(f"[LABELS] Found {len(all_spendings)} spendings with labels for user {current_user.id}")
    print(f"[LABELS] Labels found: {[s.label for s in all_spendings]}")
    
    # Get all unique labels for the user with improved filtering
    unique_labels_query = db.query(Spending.label).filter(
        Spending.user_id == current_user.id,
        Spending.label.isnot(None),
        func.trim(Spending.label) != ""
    ).distinct()
    
    unique_labels = unique_labels_query.all()
    
    # Debug the labels we found
    label_values = [l[0] for l in unique_labels if l[0] and l[0].strip()]
    print(f"[LABELS] Found {len(label_values)} unique labels: {label_values}")
    
    labels_stats = []
    
    # Iterate through each unique label
    for label_tuple in unique_labels:
        label = label_tuple[0]
        if not label or label.strip() == "":
            continue
            
        # Get all spendings for this label
        label_spendings = db.query(Spending).filter(
            Spending.user_id == current_user.id,
            Spending.label == label
        ).all()
        
        if not label_spendings:
            print(f"[LABELS] No spendings found for label '{label}'")
            continue
        
        # Calculate statistics
        total_spending = sum(s.amount for s in label_spendings)
        transaction_count = len(label_spendings)
        average_per_transaction = total_spending / transaction_count if transaction_count > 0 else 0
        
        # Find highest spending transaction
        highest_spending = max(label_spendings, key=lambda s: s.amount)
        highest_spending_amount = highest_spending.amount
        highest_spending_date = highest_spending.date
        
        # Get date range
        dates = [s.date for s in label_spendings]
        first_transaction_date = min(dates)
        last_transaction_date = max(dates)
        
        # Get top categories for this label
        category_totals = {}
        for spending in label_spendings:
            if spending.category in category_totals:
                category_totals[spending.category] += spending.amount
            else:
                category_totals[spending.category] = spending.amount
        
        top_categories = [
            {"category": cat, "amount": amount}
            for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        ]
        
        label_stat = LabelStats(
            label=label,
            total_spending=total_spending,
            transaction_count=transaction_count,
            average_per_transaction=average_per_transaction,
            highest_spending_date=highest_spending_date,
            highest_spending_amount=highest_spending_amount,
            first_transaction_date=first_transaction_date,
            last_transaction_date=last_transaction_date,
            top_categories=top_categories,
            currency=current_user.preferred_currency
        )
        
        labels_stats.append(label_stat)
    
    # Sort by total spending (highest first)
    labels_stats.sort(key=lambda x: x.total_spending, reverse=True)
    
    print(f"[LABELS] Found {len(labels_stats)} labels for user {current_user.id}")
    
    return LabelsOverview(
        total_labels=len(labels_stats),
        labels_stats=labels_stats
    )

@router.get("/{label_name}", response_model=LabelStats)
async def get_label_details(
    label_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed statistics for a specific label"""
    ensure_label_column(db)
    print(f"[LABELS] Getting details for label '{label_name}' for user {current_user.id}")
    
    # Get all spendings for this label with more reliable matching
    label_spendings = db.query(Spending).filter(
        Spending.user_id == current_user.id,
        func.trim(Spending.label) == label_name.strip()
    ).all()
    
    print(f"[LABELS] Found {len(label_spendings)} spendings with label '{label_name}'")
    
    if not label_spendings:
        raise HTTPException(status_code=404, detail="Label not found")
    
    # Calculate statistics
    total_spending = sum(s.amount for s in label_spendings)
    transaction_count = len(label_spendings)
    average_per_transaction = total_spending / transaction_count if transaction_count > 0 else 0
    
    # Find highest spending transaction
    highest_spending = max(label_spendings, key=lambda s: s.amount)
    highest_spending_amount = highest_spending.amount
    highest_spending_date = highest_spending.date
    
    # Get date range
    dates = [s.date for s in label_spendings]
    first_transaction_date = min(dates)
    last_transaction_date = max(dates)
    
    # Get top categories for this label
    category_totals = {}
    for spending in label_spendings:
        if spending.category in category_totals:
            category_totals[spending.category] += spending.amount
        else:
            category_totals[spending.category] = spending.amount
    
    top_categories = [
        {"category": cat, "amount": amount}
        for cat, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    ]
    
    return LabelStats(
        label=label_name,
        total_spending=total_spending,
        transaction_count=transaction_count,
        average_per_transaction=average_per_transaction,
        highest_spending_date=highest_spending_date,
        highest_spending_amount=highest_spending_amount,
        first_transaction_date=first_transaction_date,
        last_transaction_date=last_transaction_date,
        top_categories=top_categories,
        currency=current_user.preferred_currency
    )
