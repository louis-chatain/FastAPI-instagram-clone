from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.database import Base, engine
from router import comment, post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)

Base.metadata.create_all(engine)

app.mount("/database/files", StaticFiles(directory="database/files"), name="files")  # makes files statically available
