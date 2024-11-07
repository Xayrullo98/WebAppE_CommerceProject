from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
from schemas.users import UserCurrent
from schemas.branch import BranchCreate
Base.metadata.create_all(bind=engine)

from functions.branch import  all_branchs,  create_branch, one_branch



router_branch = APIRouter()


@router_branch.post('/add', )
async def add_branch(form:BranchCreate, db: Session = Depends(get_db),
             current_user: UserCurrent = Depends(get_current_active_user)):
    return await create_branch(form, current_user, db)



@router_branch.get('/', status_code=200)
async def get_branch(status: bool = None, id: int = 0, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return await one_branch(id, db)
    else:
        return await all_branchs(status=status, page=page, limit=limit, db=db)



