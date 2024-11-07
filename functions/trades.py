import datetime
from pprint import pprint

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import  joinedload

from functions.basket import one_basket
from functions.orders import one_order
from functions.products import one_product
from functions.sold_products import create_sold_product
from functions.users import one_user
from models.trades import Trades
from utils.pagination import pagination

async def all_trades(status, trade_status, order_id, user_id, page, limit, db):


    if status in [True, False]:
        status_filter = Trades.status == status
    else:
        status_filter = Trades.id>0
    if trade_status in [True, False]:
        trade_status_filter = Trades.trade_status == trade_status
    else:
        trade_status_filter = Trades.id > 0
    if order_id:
        order_filter = Trades.order_id == order_id
    else:
        order_filter = Trades.order_id > 0

    if user_id:
        user_filter = Trades.user_id == user_id
    else:
        user_filter = Trades.user_id > 0

    trades = db.query(Trades).options(joinedload(Trades.order),
                                      joinedload(Trades.sold_product),
                                      joinedload(Trades.user),
                                      ).filter(
        status_filter,
        order_filter,
        user_filter,
        trade_status_filter
    ).order_by(Trades.id.desc())

    if page and limit:
        return pagination(trades, page, limit)
    else:
        return trades.all()


async def one_trade(id, db):
    data = db.query(Trades).options(joinedload(Trades.order), joinedload(Trades.user),joinedload(Trades.product)).filter(
        Trades.id == id).order_by(Trades.id.desc()).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data

async def last_trade(user_id, db):
    return db.query(Trades).filter(Trades.user_id == user_id).order_by(Trades.id.desc()).first()



async def create_trade(forms, order_id, user, db):
    try:
        trades_list = []
        for form in forms:
            basket = await one_basket(form.id,db)
            product = await one_product(basket.product_id,db)

            sold_product = await create_sold_product(user=user,db=db,code=product.code,id_number=product.id_number,name=product.name,number=product.number,is_ordered=product.is_ordered,price100=product.price100,price25=product.price25,percentage=product.percentage,deadline=product.deadline,company_name=product.company_name,branch_id=product.branch_id)
            new_trade_db = Trades(
                order_id=order_id,
                product_id=sold_product.id,
                user_id=user.id,
                number=basket.number,
            )
            trades_list.append(new_trade_db)

        # Use add_all to add multiple objects
        db.add_all(trades_list)

        # Commit the transaction asynchronously
        db.commit()

        # Refresh each trade in trades_list
        for trade in trades_list:
            db.refresh(trade)

        return 1
    except SQLAlchemyError as x:
        # Capture specific SQLAlchemy errors
        db.rollback()  # Rollback the transaction in case of error
        raise HTTPException(status_code=400, detail=f"Database error: {x}")
    except Exception as x:
        # Handle any other exceptions
        db.rollback()  # Rollback for any other exceptions as well
        raise HTTPException(status_code=400, detail=f"Error: {x}")




async def update_trade(form, user, db):
    await one_trade(form.trade_id, db)
    await one_user(user.id, db)
    await one_order(user.order_id, db)
    await one_product(user.product_id, db)

    db.query(Trades).filter(Trades.id == form.id).update({
        Trades.id: form.id,
        Trades.user_id: user.id,
        Trades.order_id: form.order_id,
        Trades.product_id: form.product_id,
        Trades.number: form.number,
        })
    db.commit()

    return one_trade(form.id, db)




