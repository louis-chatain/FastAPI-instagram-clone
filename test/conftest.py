# tests/conftest.py

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from main import app
from database.database import get_db, Base

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test/test.db"

@pytest.fixture(scope="session")
def engine():
    db_engine: Engine =  create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    try:
        yield db_engine
    finally:
        db_engine.dispose()

@pytest.fixture(scope="function")
def session(engine: Engine):
    try: # Clean up the database before each test
        Base.metadata.drop_all(bind=engine)
    finally:
        # Create the tables and a new session for each test
        Base.metadata.create_all(bind=engine)
        TestingSessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db: Session = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            

@pytest.fixture(scope="function")
def client(session: Session):
    # Override the dependency with the test session
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    # Yield a test client that uses the overridden dependency
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

    # Clean up the override
    app.dependency_overrides.clear()