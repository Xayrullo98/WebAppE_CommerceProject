from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class SoldProductBase(BaseModel):
    code: Optional[int] = Field(title="code")
    id_number: Optional[int] = Field(title="id_number")
    name: Optional[int] = Field(title="name")
    number: Optional[int] = Field(title="number")
    is_ordered: Optional[int] = Field(title="is_ordered")
    price100: Optional[int] = Field(title="price100")
    price25: Optional[int] = Field(title="price25")
    percentage: Optional[int] = Field(title="percentage")
    deadline: Optional[datetime] = Field(title="deadline")
    company_name: Optional[int] = Field(title="company_name")
    status: Optional[int] = Field(title="status")
    branch_id: Optional[int] = Field(title="Branch_id")

class SoldProductCreate(SoldProductBase):
    pass


class SoldProductUpdate(SoldProductBase):
    id: int
    status: bool
