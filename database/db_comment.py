from fastapi import HTTPException, status
from database.models import DbComment
from schemas.schemas_auth import UserAuth
from schemas.schemas_comment import CommentModel, CommentUpdateModel
from sqlalchemy.orm.session import Session
from datetime import datetime
from sqlalchemy import exc


def create(request: CommentModel, current_user: UserAuth, db: Session):
    try:
        new_comment = DbComment(
            text = request.text,
            timestamp = datetime.now().date(),
            user_id = current_user.id,
            post_id = request.post_id,
        )
        db.add(new_comment)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database.",
        )
    return new_comment


def read_all(db: Session):
    comments = db.query(DbComment).all()
    return comments


def read_by_id(id: str, db: Session):
    comment = db.query(DbComment).filter(DbComment.id == id)
    return comment


def update(request: CommentUpdateModel, current_user: UserAuth, db: Session):
    comment = db.query(DbComment).filter(DbComment.id == request.id, DbComment.user_id == current_user.id)
    if not comment.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {current_user.id} is not authorized to update comment with id {id}, or the comment does not exist.",
        )
    
    try:
        comment.update(
            {
                DbComment.text: request.text,
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
    comment = db.query(DbComment).filter(DbComment.id == request.id).first()
    return comment


def delete(id: int, current_user: UserAuth, db: Session):
    comment = db.query(DbComment).filter(DbComment.id == id, DbComment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {id} in the database."
        )
    try:
        db.delete(comment)
        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        print(f"Database error during deletion: {e}")
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving changes to the database."
        )
    return comment