
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import  Session

from db import SessionLocal
from functions.users import one_user
from models.products import Products
from utils.pagination import pagination


async def all_products(search, status,branch_id, company_name,  page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Products.name.ilike(search_formatted)| Products.company_name.ilike(search_formatted)
    else:
        search_filter = Products.id > 0
    if status in [True, False]:
        status_filter = Products.status == status
    else:
        status_filter = Products.id>0

    if company_name:
        order_filter = Products.company_name == company_name
    else:
        order_filter = Products.id > 0

    if branch_id:
        branch_filter = Products.branch_id == branch_id
    else:
        branch_filter = Products.id > 0

    products = db.query(Products).filter(
        status_filter,
        order_filter,
        search_filter,
        branch_filter
    ).order_by(Products.id.desc())

    if page and limit:
        return pagination(products, page, limit)
    else:
        return products.all()


async def one_product(id, db):
    data =  db.query(Products).filter(
        Products.id == id).order_by(Products.id.desc()).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data

async def create_product(form, user, db):
    await one_user(user.id, db)
    new_order_db = Products(
            code=form.code,
            id_number=form.id_number,
            name=form.name,
            number=form.number,
            is_ordered=form.is_ordered,
            price100=form.price100,
            price25=form.price25,
            percentage=form.percentage,
            deadline=form.deadline,
            company_name=form.company_name,
            branch_id=form.branch_id )
    db.add(new_order_db)
    db.commit()
    db.refresh(new_order_db)
    return new_order_db

def add_product(code, id_number, name, number, is_ordered, price100, price25, percentage, deadline, company_name, branch_id):
    db = SessionLocal()
    product = db.query(Products).filter(Products.branch_id==branch_id,Products.code==code).first()
    if product:
        return None
    try:
        if str(price100).lower() =='nan' or price100 is None:
            return None
        new_order_db = Products(
            code=code,
            id_number=id_number,
            name=name,
            number=number,
            is_ordered=is_ordered,
            price100=float(price100),
            price25=float(price25),
            percentage=percentage,
            deadline=deadline,
            company_name=company_name,
            branch_id=branch_id
        )

        db.add(new_order_db)
        db.commit()
        db.refresh(new_order_db)
        return new_order_db
    except ValueError :
        pass
    except IntegrityError:
        pass
    except Exception as e:
        db.rollback()
        print(f"Error adding product: {e}")
    finally:
        db.close()

async def update_product(form, user, db):
    await one_product(form.id, db)
    await one_user(user.id, db)

    db.query(Products).filter(Products.id == form.id).update({
        Products.id: form.id,
        Products.code: form.code,
        Products.id_number: form.id_number,
        Products.name: form.name,
        Products.number: form.number,
        Products.is_ordered: form.is_ordered,
        Products.price100: form.price100,
        Products.price25: form.price25,
        Products.percentage: form.percentage,
        Products.deadline: form.deadline,
        Products.company_name: form.company_name,
        Products.status: form.status})
    db.commit()

    return one_product(form.id, db)


def update_product_for_db(id, code,id_number,name,number,is_ordered,price100,price25,percentage,deadline,company_name):
    db:Session = SessionLocal()
    db.query(Products).filter(Products.id == id).update({
        Products.code: code,
        Products.id_number: id_number,
        Products.name: name,
        Products.number: number,
        Products.is_ordered: is_ordered,
        Products.price100: price100,
        Products.price25: price25,
        Products.percentage: percentage,
        Products.deadline: deadline,
        Products.company_name: company_name,
    })
    db.commit()

    return  True



def products(branch_id):
    db = SessionLocal()
    return db.query(Products).filter(Products.branch_id==branch_id).all()

def delete_product(code):
    db = SessionLocal()
    stmt = delete(Products).where(Products.code==code)
    result = db.execute(stmt)
    db.commit()
    return  True
def check_product(code,branch_id):
    db = SessionLocal()
    all_codes = db.query(Products.code).filter(Products.branch_id==branch_id).all()
    if code in all_codes:
        return True
    return False


