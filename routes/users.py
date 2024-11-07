from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.users import one_user, all_users, update_user, create_user, user_current

from schemas.users import UserCreate, UserUpdate, UserCurrent

router_user = APIRouter()


@router_user.post('/add', )
async def add_user(form: UserCreate, db: Session = Depends(get_db),
             ):  #
    if await  create_user(form=form,user=1, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_user.get('/', status_code=200)
async def get_users(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 20,
              db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return await one_user(id, db)
    else:
        return await all_users(search, status, page, limit, db)


@router_user.get('/user', status_code=200)
async def get_user_current(db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if current_user:
        return await user_current(current_user, db)


@router_user.put("/update")
async def user_update(form: UserUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if await update_user(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
