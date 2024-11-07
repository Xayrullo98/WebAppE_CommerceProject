from sqlalchemy import Column, Integer, String, Boolean,Float,Text
from sqlalchemy.orm import relationship

from db import Base




class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    balance = Column(Float, nullable=True,default=0)
    status = Column(Boolean, nullable=True, default=True)
    token = Column(String(400), default='',nullable=True)
    branch_id = Column(Integer,nullable=True,default=0)

    trade = relationship("Trades", back_populates="user")
    order = relationship("Orders", back_populates="user")