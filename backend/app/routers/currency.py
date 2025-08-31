from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.currency import currency_service
from app.schemas import CurrencyInfo, CurrencyConversion
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api", tags=["currency"])

@router.get("/currencies", response_model=List[CurrencyInfo])
async def get_currencies():
    """Get list of supported currencies"""
    return currency_service.get_supported_currencies()

@router.get("/exchange-rate/{from_currency}/{to_currency}")
async def get_exchange_rate(
    from_currency: str, 
    to_currency: str,
    current_user: User = Depends(get_current_user)
):
    """Get exchange rate between two currencies"""
    rate = await currency_service.get_exchange_rate(from_currency.upper(), to_currency.upper())
    
    if rate is None:
        raise HTTPException(
            status_code=400, 
            detail=f"Unable to get exchange rate from {from_currency} to {to_currency}"
        )
    
    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "rate": rate,
        "timestamp": currency_service.cache.get(f"{from_currency.upper()}_{to_currency.upper()}", {}).get("timestamp")
    }

@router.post("/convert", response_model=CurrencyConversion)
async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    current_user: User = Depends(get_current_user)
):
    """Convert amount from one currency to another"""
    conversion = await currency_service.convert_amount(
        amount, 
        from_currency.upper(), 
        to_currency.upper()
    )
    
    if conversion is None:
        raise HTTPException(
            status_code=400, 
            detail=f"Unable to convert from {from_currency} to {to_currency}"
        )
    
    return conversion
