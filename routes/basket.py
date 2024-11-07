from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.basket import BasketCreate, BasketUpdate
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions.basket import all_basket, create_basket, one_basket, update_basket

router_basket = APIRouter()


@router_basket.post('/add', )
async def add_basket( form:BasketCreate, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    return await create_basket(form=form,user=current_user, db=db)



@router_basket.get('/', status_code=200)
async def get_basket(status: bool = None, id: int = 0, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await one_basket(id, db)
    else:
        return await all_basket(status=status,user_id=current_user.id, page=page, limit=limit, db=db)



@router_basket.put("/update")
async def basket_update(form: BasketUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if await update_basket(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
