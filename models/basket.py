from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func,Float
from sqlalchemy.orm import relationship

from db import Base

class Basket(Base):
    __tablename__ = "Basket"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)
    number = Column(Integer , nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean,nullable=True, default=None)



