from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_comment():
    response = client.get("/comment/read_all")
    assert response.status_code == 200