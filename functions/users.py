
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'])
from fastapi import HTTPException
from models.users import Users

from routes.auth import get_password_hash
from utils.pagination import pagination


async def all_users(search, status, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Users.name.like(search_formatted) | Users.username.like(
            search_formatted)
    else:
        search_filter = Users.id > 0
    if status in [True, False]:
        status_filter = Users.status == status
    else:
        status_filter = Users.id > 0



    users = db.query(Users).filter(search_filter, status_filter).order_by(Users.name.asc())
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


async def one_user(id, db):
    data = db.query(Users).filter(Users.id == id).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data


async def user_current(user, db):
    return db.query(Users).filter(Users.id == user.id).first()


async def create_user(form, user, db):
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")


    new_user_db = Users(
        name=form.name,
        username=form.username,
        password=get_password_hash(form.password),

    )
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user_db


async def update_user(form, user, db):
    if await one_user(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.balance: form.balance,
        Users.password: get_password_hash(form.password),

    })
    db.commit()

    return await one_user(form.id, db)









