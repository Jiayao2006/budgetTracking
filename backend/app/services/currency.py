import httpx
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.schemas import CurrencyInfo, ExchangeRate, CurrencyConversion

class CurrencyService:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4"
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache rates for 1 hour
        
        # Popular currencies with their symbols
        self.currencies = {
            "USD": {"name": "US Dollar", "symbol": "$"},
            "EUR": {"name": "Euro", "symbol": "€"},
            "GBP": {"name": "British Pound", "symbol": "£"},
            "JPY": {"name": "Japanese Yen", "symbol": "¥"},
            "AUD": {"name": "Australian Dollar", "symbol": "A$"},
            "CAD": {"name": "Canadian Dollar", "symbol": "C$"},
            "CHF": {"name": "Swiss Franc", "symbol": "CHF"},
            "CNY": {"name": "Chinese Yuan", "symbol": "¥"},
            "INR": {"name": "Indian Rupee", "symbol": "₹"},
            "KRW": {"name": "South Korean Won", "symbol": "₩"},
            "SGD": {"name": "Singapore Dollar", "symbol": "S$"},
            "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$"},
            "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$"},
            "SEK": {"name": "Swedish Krona", "symbol": "kr"},
            "NOK": {"name": "Norwegian Krone", "symbol": "kr"},
            "MXN": {"name": "Mexican Peso", "symbol": "$"},
            "BRL": {"name": "Brazilian Real", "symbol": "R$"},
            "ZAR": {"name": "South African Rand", "symbol": "R"},
            "THB": {"name": "Thai Baht", "symbol": "฿"},
            "MYR": {"name": "Malaysian Ringgit", "symbol": "RM"},
        }

    def get_supported_currencies(self) -> List[CurrencyInfo]:
        """Get list of supported currencies"""
        return [
            CurrencyInfo(code=code, name=info["name"], symbol=info["symbol"])
            for code, info in self.currencies.items()
        ]

    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get exchange rate from one currency to another"""
        if from_currency == to_currency:
            return 1.0

        cache_key = f"{from_currency}_{to_currency}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data["timestamp"] < self.cache_duration:
                return cached_data["rate"]

        try:
            async with httpx.AsyncClient() as client:
                # Use free tier of exchangerate-api.com
                url = f"{self.base_url}/latest/{from_currency}"
                response = await client.get(url, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    rates = data.get("rates", {})
                    
                    if to_currency in rates:
                        rate = rates[to_currency]
                        
                        # Cache the result
                        self.cache[cache_key] = {
                            "rate": rate,
                            "timestamp": datetime.now()
                        }
                        
                        return rate
                
                return None
                
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    async def convert_amount(self, amount: float, from_currency: str, to_currency: str) -> Optional[CurrencyConversion]:
        """Convert amount from one currency to another"""
        rate = await self.get_exchange_rate(from_currency, to_currency)
        
        if rate is None:
            return None
            
        converted_amount = round(amount * rate, 2)
        
        return CurrencyConversion(
            original_amount=amount,
            original_currency=from_currency,
            target_currency=to_currency,
            converted_amount=converted_amount,
            exchange_rate=rate
        )

    def get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol for display"""
        return self.currencies.get(currency_code, {}).get("symbol", currency_code)

    def format_amount(self, amount: float, currency_code: str) -> str:
        """Format amount with currency symbol"""
        symbol = self.get_currency_symbol(currency_code)
        
        # Special formatting for different currencies
        if currency_code == "JPY" or currency_code == "KRW":
            # No decimal places for these currencies
            return f"{symbol}{amount:,.0f}"
        else:
            return f"{symbol}{amount:,.2f}"

# Global instance
currency_service = CurrencyService()
