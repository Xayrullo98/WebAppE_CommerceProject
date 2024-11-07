from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float,Text
from sqlalchemy.orm import relationship

from db import Base



class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    money = Column(Integer, nullable=True)
    payment_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    status = Column(Integer, nullable=True, default=0)

    trade = relationship("Trades", back_populates="order")
    user = relationship("Users", back_populates="order")
    result  = relationship("Result", back_populates="order")
