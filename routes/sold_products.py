from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.sold_products import SoldProductBase,SoldProductUpdate
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions.sold_products import all_sold_products, create_sold_product, one_sold_product,update_sold_product

router_sold_product = APIRouter()


@router_sold_product.post('/add', )
async def add_sold_product(form:SoldProductBase, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    return await create_sold_product(form,current_user, db)


@router_sold_product.get('/', status_code=200)
async def get_sold_products(search:str =None, status: bool = None,company_name:str=None, branch_id:int=0,order_id:int=0, id: int = 0, page: int = 1, limit: int = 25,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await one_sold_product(id, db)
    else:
        return await all_sold_products(search=search, status=status,branch_id=branch_id,order_id=order_id, company_name=company_name, page=page, limit=limit, db=db)



@router_sold_product.put("/update")
async def sold_product_update(form: SoldProductUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if await update_sold_product(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
