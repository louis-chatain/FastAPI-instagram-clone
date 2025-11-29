from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import db_user
from database.database import get_db
from schemas.schemas_user import UserDisplay, UserModel


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserDisplay)
def create(request: UserModel, db: Session = Depends(get_db)):
    user = db_user.create(request, db)
    return user

@router.get("/real_all", response_model=List[UserDisplay])
def read_all(db: Session = Depends(get_db)):
    users = db_user.read_all(db)
    return users

@router.put("/update", response_model=UserDisplay)
def update(id: int, request: UserModel, db: Session = Depends(get_db)):
    user = db_user.update(id, request, db)
    return user

@router.delete("/delete", response_model=UserDisplay)
def delete(id: int, db: Session = Depends(get_db)):
    deleted_user = db_user.delete(id, db)
    return deleted_user