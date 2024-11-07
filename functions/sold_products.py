from tracemalloc import Trace

from fastapi import HTTPException, Depends
from sqlalchemy.orm import joinedload, Session

from db import get_db, SessionLocal
from functions.users import one_user
from models.orders import Orders
from models.sold_products import SoldProducts
from models.trades import Trades
from utils.pagination import pagination


async def all_sold_products(search, status,branch_id, order_id, company_name,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = SoldProducts.name.ilike(search_formatted)| SoldProducts.company_name.ilike(search_formatted)
    else:
        search_filter = SoldProducts.id > 0
    if status in [True, False]:
        status_filter = SoldProducts.status == status
    else:
        status_filter = SoldProducts.id>0

    if company_name:
        company_filter = SoldProducts.company_name == company_name
    else:
        company_filter = SoldProducts.id > 0

    if branch_id:
        branch_filter = SoldProducts.branch_id == branch_id
    else:
        branch_filter = SoldProducts.id > 0
    if order_id:
        sold_products = (db.query(SoldProducts)
                         .join(Trades).join(Orders, Trades.order_id == order_id).filter(
            status_filter,
            search_filter,
            branch_filter,
            company_filter
        ).order_by(SoldProducts.id.desc()))
    else:
        sold_products = (db.query(SoldProducts).filter(
            status_filter,
            search_filter,
            branch_filter,
            company_filter
        ).order_by(SoldProducts.id.desc()))

    if page and limit:
        return pagination(sold_products, page, limit)
    else:
        return sold_products.all()


async def one_sold_product(id, db):
    data =  db.query(SoldProducts).filter(
        SoldProducts.id == id).order_by(SoldProducts.id.desc()).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data

async def create_sold_product(code,id_number,name,number,is_ordered,price100,price25,percentage,deadline,company_name,branch_id, user, db):
    await one_user(user.id, db)
    new_order_db = SoldProducts(
            code=code,
            id_number=id_number,
            name=name,
            number=number,
            is_ordered=is_ordered,
            price100=price100,
            price25=price25,
            percentage=percentage,
            deadline=deadline,
            company_name=company_name,
            branch_id=branch_id )
    db.add(new_order_db)
    db.commit()
    db.refresh(new_order_db)
    return new_order_db

def add_sold_product(code, id_number, name, number, is_ordered, price100, price25, percentage, deadline, company_name, branch_id):
    # Step 2: Create a new session from the sessionmaker
    db = SessionLocal()
    try:
        # Step 3: Create a new SoldProducts instance
        new_order_db = SoldProducts(
            code=code,
            id_number=id_number,
            name=name,
            number=number,
            is_ordered=is_ordered,
            price100=price100,
            price25=price25,
            percentage=percentage,
            deadline=deadline,
            company_name=company_name,
            branch_id=branch_id
        )
        # Step 4: Add the new product to the session and commit
        db.add(new_order_db)
        db.commit()
        db.refresh(new_order_db)
        return new_order_db
    except Exception as e:
        # Step 5: Rollback the session in case of an error
        db.rollback()
        print(f"Error adding product: {e}")  # Log the error for debugging
        raise e  # Optionally re-raise the exception if you want to handle it further up the call stack
    finally:
        # Step 6: Close the session
        db.close()

async def update_sold_product(form, user, db):
    await one_sold_product(form.id, db)
    await one_user(user.id, db)

    db.query(SoldProducts).filter(SoldProducts.id == form.id).update({
        SoldProducts.id: form.id,
        SoldProducts.code: form.code,
        SoldProducts.id_number: form.id_number,
        SoldProducts.name: form.name,
        SoldProducts.number: form.number,
        SoldProducts.is_ordered: form.is_ordered,
        SoldProducts.price100: form.price100,
        SoldProducts.price25: form.price25,
        SoldProducts.percentage: form.percentage,
        SoldProducts.deadline: form.deadline,
        SoldProducts.company_name: form.company_name,
        SoldProducts.status: form.status})
    db.commit()

    return one_sold_product(form.id, db)




