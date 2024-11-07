
from fastapi import HTTPException
from functions.products import one_product
from functions.users import one_user
from models.basket import Basket
from utils.pagination import pagination
from sqlalchemy import delete

async def all_basket(status, user_id, page, limit, db):


    if status in [True, False]:
        status_filter = Basket.status == status
    else:
        status_filter = Basket.id>0   

    if user_id:
        user_filter = Basket.user_id == user_id
    else:
        user_filter = Basket.user_id > 0

    basket = db.query(Basket).filter(
        status_filter,
        user_filter,
    ).order_by(Basket.id.desc())

    if page and limit:
        return pagination(basket, page, limit)
    else:
        return basket.all()


async def one_basket(id, db):
    basket =  db.query(Basket).filter(
        Basket.id == id).order_by(Basket.id.desc()).first()
    if not basket:
        raise HTTPException(status_code=400, detail="Bunday id raqamli basket mavjud emas")
    return basket

async def create_basket(form, user, db):
    await one_user(user.id, db)
    await one_product(form.product_id, db)

    try:         
        new_basket_db = Basket(
           product_id=form.product_id,
           number=form.number,
           user_id=user.id,
            )
        db.add(new_basket_db)
        db.commit()
        db.refresh(new_basket_db)
        return new_basket_db
    except Exception as x:
        raise HTTPException(status_code=400, detail=f"{x}")




async def update_basket(form, user, db):
    await one_basket(form.id, db)
    await one_user(user.id, db)
    await one_product(form.product_id, db)

    if form.number==0:
        await delete_basket([form.id],user.id, db)
        return {"data":"data deleted"}
    db.query(Basket).filter(Basket.id == form.id).update({
        Basket.id: form.id,
        Basket.user_id: user.id,
        Basket.product_id: form.product_id,
        Basket.number: form.number})
    db.commit()

    return one_basket(form.id, db)





async def delete_basket(ids_list, user_id, db):
    stmt = delete(Basket).where(Basket.id.in_(ids_list), Basket.user_id == user_id)
    result = db.execute(stmt)
    db.commit()
    return {"data": f"{result.rowcount} records deleted"}
