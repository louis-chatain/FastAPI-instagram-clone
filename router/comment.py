from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import db_comment
from database.database import get_db
from schemas.schemas_comment import CommentDisplay, CommentModel

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("/create", response_model=CommentDisplay)
def create(request: CommentModel, db: Session = Depends(get_db)):
    comment = db_comment.create(request, db)
    return comment


@router.get("/real_all", response_model=List[CommentDisplay])
def read_all(db: Session = Depends(get_db)):
    comment = db_comment.read_all(db)
    return comment


@router.put("/update", response_model=CommentDisplay)
def update(id: int, request: CommentModel, db: Session = Depends(get_db)):
    comment = db_comment.update(id, request, db)
    return comment


@router.delete("/delete", response_model=CommentDisplay)
def delete(id: int, db: Session = Depends(get_db)):
    deleted_comment = db_comment.delete(id, db)
    return deleted_comment
