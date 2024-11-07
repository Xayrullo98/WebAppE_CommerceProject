
from fastapi import HTTPException

from functions.users import one_user
from models.branch import Branch

from utils.pagination import pagination


async def all_branchs(status, page, limit, db):

    if status in [True, False]:
        status_filter = Branch.status == status
    else:
        status_filter = Branch.id>0



    branchs = db.query(Branch).filter(status_filter).order_by(
        Branch.id.desc())
    if page and limit:
        return pagination(branchs, page, limit)

    else:
        return branchs.all()


async def one_branch(id, db):
    data = db.query(Branch).filter(Branch.id == id).first()
    if not data:
        raise HTTPException(status_code=400, detail="Bunday id raqamli malumot mavjud emas")
    return data


async def create_branch(form, cur_user, db):
    await one_user(cur_user.id, db)
    new_branch_db = Branch(
        name=form.name,
        user_id=cur_user.id,
    )
    db.add(new_branch_db)
    db.commit()
    db.refresh(new_branch_db)

    return new_branch_db


async def update_branch(form, cur_user, db):
    await one_branch(form.id, db)
    await one_user(cur_user.id, db)

    db.query(Branch).filter(Branch.id == form.id).update({
        Branch.name: form.name,
        Branch.user_id: cur_user.id,
        Branch.status: form.status
    })
    db.commit()
    return one_branch(form.id, db)
