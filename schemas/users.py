
from pydantic import BaseModel
from typing import Optional, List




class UserBase(BaseModel):
    name: str
    username: str
    password: str


class UserCreate(UserBase):
    pass



class UserUpdate(UserBase):
    id: int
    balance: float





class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: Optional[str] = None

class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    status: bool