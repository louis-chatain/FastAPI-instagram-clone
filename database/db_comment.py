from fastapi import HTTPException, status
from database.models import DbComment
from schemas.schemas_comment import CommentModel
from sqlalchemy.orm.session import Session
from datetime import datetime


def create(request: CommentModel, db: Session):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        timestamp = datetime.now().date()
    )
    db.add(new_comment)
    db.commit()
    return new_comment


def read_all(db: Session):
    comments = db.query(DbComment).all()
    return comments


def read_by_id(id: str, db: Session):
    comment = db.query(DbComment).filter_by(id=id)
    return comment


def update(id: str, request: CommentModel, db: Session):
    post = db.query(DbComment).filter_by(id=id)
    post.update(
        {
            DbComment.text: request.text,
            DbComment.username: request.username,
        }
    )
    db.commit()
    comment = db.query(DbComment).filter_by(id=id).first()
    return comment


def delete(id: int, db: Session):
    comment = db.query(DbComment).filter_by(id=id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with the id {id} in the database.")
    db.delete(comment)
    db.commit()
    return comment