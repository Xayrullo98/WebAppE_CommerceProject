from typing import Optional,List
from pydantic import BaseModel,Field

from schemas.basket import  BasketAdd


class OrderBase(BaseModel):
    basket: List[BasketAdd] = Field(title="Basket")
    payment_type: str = Field(title="Payment_type")



class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: int
    status: bool
