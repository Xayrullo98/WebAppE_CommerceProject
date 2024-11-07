from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session
from schemas.products import ProductUpdate

from routes.auth import get_current_active_user
from schemas.products import ProductBase
from schemas.users import UserCurrent

Base.metadata.create_all(bind=engine)

from functions.products import all_products, create_product, one_product,update_product

router_product = APIRouter()


@router_product.post('/add', )
async def add_product(form:ProductBase, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    return await create_product(form,current_user, db)


@router_product.get('/', status_code=200)
async def get_products(search:str =None, status: bool = None,company_name:str=None, branch_id:int=0, id: int = 0, page: int = 1, limit: int = 25,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await one_product(id, db)
    else:
        return await all_products(search=search, status=status,branch_id=branch_id, company_name=company_name, page=page, limit=limit, db=db)



@router_product.put("/update")
async def product_update(form: ProductUpdate, db: Session = Depends(get_db),
                current_user: UserCurrent = Depends(get_current_active_user)):
    if await update_product(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
