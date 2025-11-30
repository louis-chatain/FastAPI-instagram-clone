from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from werkzeug.security import check_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from auth.oauth2 import create_access_token
from database.database import get_db
from database.models import DbUser


router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials."
        )
    
    pwd = check_password_hash(user.hashed_password, request.password)
    if pwd == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password."
        )

    access_token = create_access_token(data={"username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
