from datetime import datetime

from numpy.ma.extras import unique
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float,Text
from sqlalchemy.orm import relationship

from db import Base



class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    code = Column(String(50),unique=True, nullable=False)
    id_number = Column(Integer, nullable=True)
    name = Column(String(100), nullable=True)
    number = Column(Integer, nullable=True)
    is_ordered = Column(String(50), nullable=True)
    price100 = Column(Float, nullable=True)
    price25 = Column(Float, nullable=True)
    percentage = Column(String(30), nullable=True)
    deadline = Column(String(30), nullable=True)
    company_name = Column(String(100), nullable=True)
    status = Column(Boolean, nullable=True, default=None)
    branch_id = Column(Integer, ForeignKey("Branch.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

