from fastapi import HTTPException, status
from database.models import DbPost
from schemas.schemas_auth import UserAuth
from schemas.schemas_post import PostModel
from sqlalchemy.orm.session import Session
from sqlalchemy import exc
from datetime import datetime


def create(request: PostModel, current_user: UserAuth, db: Session):
    try:
        new_post = DbPost(
            image_url=request.image_url,
            image_url_type=request.image_url_type,
            caption=request.caption,
            timestamp=datetime.now().date(),
            users_id=current_user.id
        )
        db.add(new_post)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )

    return new_post


def read_all(db: Session):
    posts = db.query(DbPost).all()
    return posts


def read_current_user(db: Session, current_user: UserAuth):
    post = db.query(DbPost).filter_by(id=current_user.id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {id} found or the post does not exist.",
        )
    return post


def update(id: int, request: PostModel, current_user: UserAuth, db: Session):
    post = db.query(DbPost).filter(DbPost.users_id == current_user.id, DbPost.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.id} is not authorized to update post with id {id}, or the post does not exist.",
        )

    try:
        post.update(
            {
                DbPost.image_url: request.image_url,
                DbPost.image_url_type: request.image_url_type,
                DbPost.caption: request.caption,
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

    post = db.query(DbPost).filter(DbPost.id == id).first()
    return post


def delete(id: int, current_user: UserAuth, db: Session):
    post = db.query(DbPost).filter(DbPost.id == id, DbPost.users_id == current_user.id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.id} is not authorized to update post with id {id}, or the post does not exist.",
        )
    try:
        db.delete(post)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
    
    return post
