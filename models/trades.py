from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func,Float
from sqlalchemy.orm import relationship

from db import Base

class Trades(Base):
    __tablename__ = "Trades"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("SoldProducts.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean,nullable=True, default=None)
    trade_status = Column(Boolean, default=None,nullable=True,)
    number = Column(Float, nullable=True)

    order = relationship("Orders",back_populates="trade")
    sold_product = relationship("SoldProducts",back_populates="trade",)
    user = relationship("Users",back_populates="trade")


