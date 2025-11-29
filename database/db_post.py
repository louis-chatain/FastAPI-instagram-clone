from fastapi import HTTPException, status
from database.models import DbPost
from schemas.schemas_post import PostModel
from sqlalchemy.orm.session import Session
from datetime import datetime


def create(request: PostModel, db: Session):
    new_post = DbPost(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.now().date()
    )
    db.add(new_post)
    db.commit()
    return new_post


def read_all(db: Session):
    posts = db.query(DbPost).all()
    return posts


def read_by_id(id: str, db: Session):
    post = db.query(DbPost).filter_by(id=id)
    return post


def update(id: str, request: PostModel, db: Session):
    post = db.query(DbPost).filter_by(id=id)
    post.update(
        {
            DbPost.image_url: request.image_url,
            DbPost.image_url_type: request.image_url_type,
            DbPost.caption: request.caption,
        }
    )
    db.commit()
    post = db.query(DbPost).filter_by(id=id).first()
    return post


def delete(id: int, db: Session):
    post = db.query(DbPost).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with the id {id} in the database.")
    db.delete(post)
    db.commit()
    return post