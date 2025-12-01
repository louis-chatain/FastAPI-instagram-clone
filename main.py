from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from router import authentication, comment, post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)
app.include_router(authentication.router)

origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Access-Control-Allow-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/database/files", StaticFiles(directory="database/files"), name="files"
)  # makes files statically available

Base.metadata.create_all(engine)
