from pydantic import BaseModel


class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BranchBase):
    id: int
    status: bool
