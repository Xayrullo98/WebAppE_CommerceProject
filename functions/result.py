
from fastapi import HTTPException

from functions.users import one_user
from models.result import Result

from utils.pagination import pagination


async def all_results(status, order_id, page, limit, db):

    if status in [True, False]:
        status_filter = Result.status == status
    else:
        status_filter = Result.id>0

    if order_id:
        order_filter=Result.order_id==order_id
    else:
        order_filter=Result.id>0


    results = db.query(Result).filter(status_filter,order_filter).order_by(
        Result.id.desc())
    if page and limit:
        return pagination(results, page, limit)

    else:
        return results.all()


async def one_result(id, db):
    data = db.query(Result).filter(Result.id == id).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data


async def create_result(exist_money, absent_money, absent_products, exist_products, total_money, order_id, payment_type, cur_user, db):
    await one_user(cur_user.id, db)
    new_result_db = Result()
    db.add(new_result_db)
    db.commit()
    db.refresh(new_result_db)

    return new_result_db


async def update_result(form, cur_user, db):
    await one_result(form.id, db)
    await one_user(cur_user.id, db)

    db.query(Result).filter(Result.id == form.id).update({
        Result.name: form.name,
        Result.user_id: cur_user.id,
        Result.status: form.status
    })
    db.commit()
    return one_result(form.id, db)
