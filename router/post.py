import random
import shutil
import string
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from database import db_post
from database.database import get_db
from schemas.schemas_auth import UserAuth
from schemas.schemas_post import PostDisplay, PostModel


router = APIRouter(prefix="/post", tags=["post"])


@router.post("/create", response_model=PostDisplay)
def create(request: PostModel, db: Session = Depends(get_db)):
    post = db_post.create(request, db)
    return post

@router.get("/read_all", response_model=List[PostDisplay])
def read_all(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
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


@router.post('/image')
def upload_image(image: UploadFile = File(Ellipsis)):
  letters = string.ascii_letters
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)
  
  return {'filename': path}