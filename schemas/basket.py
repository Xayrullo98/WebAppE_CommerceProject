from typing import Optional
from pydantic import BaseModel,Field

class BasketBase(BaseModel):
    product_id: Optional[int] = Field(title="product_id")
    number: Optional[int] = Field(title="number")


class BasketCreate(BasketBase):
    pass


class BasketUpdate(BasketBase):
    id: int

class BasketAdd(BaseModel):
    id: Optional[int]