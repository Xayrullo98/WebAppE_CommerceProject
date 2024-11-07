from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.orders import OrderCreate
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions.orders import  all_orders,  create_order, one_order



router_order = APIRouter()


@router_order.post('/add', )
async def add_order( form:OrderCreate, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    return await create_order(form=form,user=current_user, db=db)



@router_order.get('/', status_code=200)
async def get_orders(status: bool = None, id: int = 0, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await one_order(id, db)
    else:
        return await all_orders(status=status,user_id=current_user.id, page=page, limit=limit, db=db)



