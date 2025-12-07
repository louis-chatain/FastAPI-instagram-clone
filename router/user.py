from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import db_user
from database.database import get_db
from schemas.schemas_user import UserDisplay, UserModel
from auth.oauth2 import get_current_user
from schemas.schemas_auth import UserAuth


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserDisplay)
def create(request: UserModel, db: Session = Depends(get_db)):
    user = db_user.create(request, db)
    return user

@router.get("/read_all", response_model=List[UserDisplay])
def read_all(db: Session = Depends(get_db)):
    users = db_user.read_all(db)
    return users

@router.put("/update", response_model=UserDisplay)
def update(request: UserModel, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    user = db_user.update(request, db, current_user)
    return user

@router.delete("/delete", response_model=UserDisplay)
def delete(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    deleted_user = db_user.delete(db, current_user)
    return deleted_user