import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------------------------  
# SQLALCHEMY_DATABASE_URL = "sqlite:///./database/instance/fastapi-instagram-clone.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# ------------------------------------------------------------------------------------  
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into os.environ
# ------------------------------------------------------------------------------------
db_url = os.getenv("DB_URL")
URL = f"{db_url}"
engine = create_engine(URL)
# ------------------------------------------------------------------------------------  

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     
Base = declarative_base()

def get_db():
    """Dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()