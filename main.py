from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.database import Base, engine
from router import post

app = FastAPI()

app.include_router(post.router)

Base.metadata.create_all(engine)

app.mount("/database/files", StaticFiles(directory="database/files"), name="files")  # makes files statically available
