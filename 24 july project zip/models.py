#SQLAlchemy Models
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship

from database import Base
#===================================================================================
# User Table
class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email    = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)

    expenses = relationship("Expense", back_populates="owner")
# ==========================
# Expense Table
# ==========================
class Expense(Base):
    __tablename__ = "expenses"

    id       = Column(Integer, primary_key=True, index=True)
    title    = Column(String(100), nullable=False)
    amount   = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    user_id  = Column(Integer, ForeignKey("users.id"))

    owner    = relationship("User", back_populates="expenses")
#=============================================================================