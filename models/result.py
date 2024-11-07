from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float,Text
from sqlalchemy.orm import relationship

from db import Base



class Result(Base):
    __tablename__ = 'Result'
    id = Column(Integer, primary_key=True)
    exist_products_number = Column(Integer, nullable=True)
    absent_products_number = Column(Integer, nullable=True)
    exist_products_money = Column(Float, nullable=True)
    absent_products_money = Column(Float, nullable=True)
    total_money = Column(Float, nullable=True)
    order_id = Column(Integer,ForeignKey('Orders.id'), nullable=True)
    payment_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    status = Column(Integer, nullable=True, default=0)

    order = relationship("Orders", back_populates="result")
