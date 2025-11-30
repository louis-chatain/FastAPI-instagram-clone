from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException, status
from database.models import DbUser
from schemas.schemas_user import UserModel
from sqlalchemy.orm.session import Session


def create(request: UserModel, db: Session):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        hashed_password=generate_password_hash(
            request.password, method="pbkdf2:sha1", salt_length=8
        ),
    )
    db.add(new_user)
    db.commit()
    return new_user


def read_all(db: Session):
    users = db.query(DbUser).all()
    return users


def read_by_id(id: str, db: Session):
    user = db.query(DbUser).filter_by(id=id)
    return user


def update(id: str, request: UserModel, db: Session):
    user = db.query(DbUser).filter_by(id=id)
    user.update(
        {
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.hashed_password: request.password,
        }
    )
    db.commit()
    user = db.query(DbUser).filter_by(id=id).first()
    return user


def delete(id: int, db: Session):
    user = db.query(DbUser).filter_by(id=id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {id} in the database.",
        )
    db.delete(user)
    db.commit()
    return user
