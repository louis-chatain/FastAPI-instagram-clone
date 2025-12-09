from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import db_comment
from database.database import get_db
from schemas.schemas_comment import CommentDisplay, CommentModel, CommentUpdateModel
from auth.oauth2 import get_current_user
from schemas.schemas_auth import UserAuth
from fastapi import status

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post(
    "/create",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Created - Comment has been created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "New Comment has been successfully added to the database."
                    }
                }
            },
        },
    }
)
def create(
    request: CommentModel,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    comment = db_comment.create(request, current_user, db)
    return comment


@router.get("/read_all", response_model=List[CommentDisplay])
def read_all(db: Session = Depends(get_db)):
    comment = db_comment.read_all(db)
    return comment


@router.put(
    "/update",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Updated - Comment has been updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Comment has been successfully updated to the database."
                    }
                }
            },
        },
    }
    )
def update(
    request: CommentUpdateModel,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    comment = db_comment.update(request, current_user, db)
    return comment


@router.delete("/delete", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    deleted_comment: None = db_comment.delete(id, current_user, db)
    return deleted_comment
