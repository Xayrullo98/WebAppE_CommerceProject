from typing import Optional
from pydantic import BaseModel,Field

class TradeBase(BaseModel):
    order_id: Optional[int] = Field(title="order_id")
    product_id: Optional[int] = Field(title="product_id")
    user_id: Optional[int] = Field(title="user_id")
    number: Optional[int] = Field(title="number")


class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    id: int
    status: bool
