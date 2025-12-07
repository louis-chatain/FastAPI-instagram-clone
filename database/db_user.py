from werkzeug.security import generate_password_hash
from fastapi import HTTPException, status
from database.models import DbUser
from schemas.schemas_auth import UserAuth
from schemas.schemas_user import UserModel
from sqlalchemy.orm.session import Session
from sqlalchemy import exc


def create(request: UserModel, db: Session):
    try:
        new_user = DbUser(
            username=request.username,
            email=request.email,
            hashed_password=generate_password_hash(
                request.password, method="scrypt:32768:8:1", salt_length=16
            ),
        )
        db.add(new_user)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )

    return new_user


def read_all(db: Session):
    users = db.query(DbUser).all()
    return users


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter_by(username=username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the username {username} in the database.",
        )
    return user


def read_by_id(id: str, db: Session):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {id} in the database.",
        )
    return user


def update(request: UserModel, db: Session, current_user: UserAuth):
    user = db.query(DbUser).filter(DbUser.id == current_user.id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.id} was not found does not exist.",
        )
    try:
        user.update(
            {
                DbUser.username: request.username,
                DbUser.email: request.email,
                DbUser.hashed_password: generate_password_hash(
                    request.password, method="scrypt:32768:8:1", salt_length=16
                ),
            }
        )
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during update: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
    user = db.query(DbUser).filter_by(id=current_user.id).first()
    return user


def delete(db: Session, current_user: UserAuth):
    user = db.query(DbUser).filter_by(id=current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {current_user.id} in the database.",
        )
    try:
        db.delete(user)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database."
        )
    return user
