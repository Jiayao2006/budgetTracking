from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    preferred_currency = Column(String(3), nullable=False, default="USD")  # User's preferred display currency
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    spendings = relationship("Spending", back_populates="user", cascade="all, delete-orphan")

class Spending(Base):
    __tablename__ = "spendings"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    original_amount = Column(Float, nullable=False)  # Original amount in input currency
    original_currency = Column(String(3), nullable=False, default="USD")  # ISO currency code
    display_currency = Column(String(3), nullable=False, default="USD")  # Currency to display in
    exchange_rate = Column(Float, nullable=False, default=1.0)  # Rate used for conversion
    category = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False, default=date.today)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="spendings")
