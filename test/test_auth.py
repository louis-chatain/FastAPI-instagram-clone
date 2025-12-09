from fastapi.testclient import TestClient

def test_auth_user(client: TestClient):
    client.post("/user/create", json={"username":"louis", "email":"louis", "password":"louis"})
    
    response = client.post("/login", data={"username":"louis", "password":"louis"})
    assert response.status_code == 200
    
def test_auth_user_wrong_password(client: TestClient):
    client.post("/user/create", json={"username":"louis", "email":"louis", "password":"louis"})
    
    response = client.post("/login", data={"username":"louis", "password":"patate"})
    assert response.status_code == 400