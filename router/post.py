from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import db_post
from database.database import get_db
from schemas.schemas_post import PostDisplay, PostModel


router = APIRouter(prefix="/post", tags=["post"])


@router.post("/create", response_model=PostDisplay)
def create(request: PostModel, db: Session = Depends(get_db)):
    post = db_post.create(request, db)
    return post

@router.get("/real_all", response_model=List[PostDisplay])
def read_all(db: Session = Depends(get_db)):
    posts = db_post.read_all(db)
    return posts

@router.put("/update", response_model=PostDisplay)
def update(id: int, request: PostModel, db: Session = Depends(get_db)):
    post = db_post.update(id, request, db)
    return post

@router.delete("/delete", response_model=PostDisplay)
def delete(id: int, db: Session = Depends(get_db)):
    deleted_post = db_post.delete(id, db)
    return deleted_post