import datetime

from fastapi import HTTPException
from sqlalchemy.orm import  joinedload

from functions.basket import delete_basket, one_basket
from functions import trades
from functions.products import one_product
from functions.users import one_user
from models.orders import Orders
from models.products import Products
from utils.pagination import pagination, NASIYA, NAQD


async def all_orders(status, user_id, page, limit, db):
    if status in [0,1,2,3]:
        status_filter = Orders.status == status
    else:
        status_filter = Orders.status.in_([0,1,2,3])

    if user_id:
        user_filter = Orders.user_id == user_id
    else:
        user_filter = Orders.user_id > 0

    orders = db.query(Orders).options(joinedload(Orders.trade)).filter(
        status_filter,
        user_filter,
    ).order_by(Orders.id.desc())

    if page and limit:
        return pagination(orders, page, limit)
    else:
        return orders.all()


async def one_order(id, db):
    data = db.query(Orders).options(joinedload(Orders.trade)).filter(
        Orders.id == id).order_by(Orders.id.desc()).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data

def last_order(db):
    return db.query(Orders).order_by(Orders.id.desc()).first()

async def create_order(form, user, db):
        await one_user(user.id, db)


        total_summa = 0
        if form.payment_type == NASIYA:
             for b in form.basket:
                 basket = await one_basket(b.id, db)
                 await one_product(basket.product_id, db)
                 product = db.query(Products.price25).filter(Products.id==basket.product_id).first()

                 number = basket.number
                 total_summa+=product.price25*number
        elif form.payment_type == NAQD:
            for b in form.basket:
                basket = await one_basket(b.id, db)
                product = db.query(Products.price100).filter(Products.id == basket.product_id).first()

                number = basket.number
                total_summa += product.price100 * number

        order = last_order(db=db)
        if order:
            number = order.number
            if number:
                number = number + 1
        else:
            number = 1
        year = datetime.datetime.now().year
        new_order_db = Orders(
            year=year,
            user_id=user.id,
            number=number,
            payment_type=form.payment_type,
            money=total_summa,
        )
        db.add(new_order_db)
        db.commit()
        db.refresh(new_order_db)
        await trades.create_trade(forms=form.basket, order_id=new_order_db.id, user=user, db=db)
        deleted = await delete_basket(ids_list=[basket.id for basket in form.basket], db=db,user_id=user.id)





        return {"total_summa":total_summa }



async def update_order(form, user, db):
    await one_order(form.id, db)
    await one_user(user.id, db)

    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.id: form.id,
        Orders.user_id: user.id,
        Orders.number: form.number,
        Orders.year: form.year,
        Orders.money: form.money})
    db.commit()

    return one_order(form.id, db)




