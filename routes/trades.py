from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from schemas.trades import TradeUpdate

from routes.auth import get_current_active_user
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions import trades

router_product = APIRouter()




@router_product.get('/', status_code=200)
async def get_trades(status: bool = None, trade_status: bool = None, order_id:int=None, id: int = 0, page: int = 1, limit: int = 20,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await trades.one_trade(id, db)
    else:
        return await trades.all_trades(status=status,trade_status=trade_status, order_id=order_id,user_id=current_user.id, page=page, limit=limit, db=db)



@router_product.put("/update")
async def product_update(form: TradeUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if trades.update_trade(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
