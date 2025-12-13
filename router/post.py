import random
import shutil
import string
from fastapi import status
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from database import db_post
from database.database import get_db
from schemas.schemas_auth import UserAuth
from schemas.schemas_post import PostDisplay, PostModel


router = APIRouter(prefix="/post", tags=["post"])


@router.post(
    "/create",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Created - User has been created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "New User has been succefully added to the database."
                    }
                }
            },
        },
    }
    )
def create(
    request: PostModel,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    post = db_post.create(request, current_user, db)
    return post


@router.get("/read_all", response_model=List[PostDisplay], status_code=status.HTTP_200_OK)
def read_all(db: Session = Depends(get_db)):
    posts = db_post.read_all(db)
    return posts


@router.get("/read_current_user", response_model=List[PostDisplay], status_code=status.HTTP_200_OK)
def read_current_user(
    db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)
):
    post = db_post.read_current_user(db, current_user)
    return post


@router.put(
    "/update",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "Forbidden - User is not the author of this post or the post does not exist.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User 123 is not authorized to update post 456."
                    }
                }
            },
        },
        404: {
            "description": "Not Found - This post was not found or does not exist in the database.",
            "content": {
                "application/json": {
                    "example": {"detail": "Post with id 123 was not found."}
                }
            },
        },
        200: {
            "description": "Updated - Post has been updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Post has been successfully updated to the database."
                    }
                }
            },
        },
    },
)
def update(
    id: int,
    request: PostModel,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    post = db_post.update(id, request, current_user, db)
    return post


@router.delete("/delete", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    deleted_post = db_post.delete(id, current_user, db)
    return deleted_post


@router.post("/image", dependencies=[Depends(get_current_user)])
def upload_image(image: UploadFile = File(Ellipsis)):
    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}
