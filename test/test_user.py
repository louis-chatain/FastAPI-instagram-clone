from fastapi.testclient import TestClient

# def test_sqlalchemyerror_create_user(client: TestClient):
#     response = client.post(
#         "/user/create", json={"": "chat", "email": "chat", "password": "chat"}
#     )
#     assert response.status_code == 500

def test_create_user(client: TestClient):
    response = client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "chat"}
    )
    assert response.status_code == 201
    response = client.get("/user/read_all")
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("username") == "chat"
    assert response.json()[0].get("email") == "chat"
    assert response.json()[0].get("posts") == []


def test_read_all_user(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "chat"}
    )
    client.post(
        "/user/create", json={"username": "cat", "email": "cat", "password": "cat"}
    )

    response = client.get("/user/read_all")

    assert response.status_code == 200
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("username") == "chat"
    assert response.json()[0].get("email") == "chat"
    assert response.json()[0].get("posts") == []

    assert response.json()[1].get("id") == 2
    assert response.json()[1].get("username") == "cat"
    assert response.json()[1].get("email") == "cat"
    assert response.json()[1].get("posts") == []


def test_update_user_while_not_logged_in(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "chat"}
    )

    response = client.put(
        "/user/update",
        json={
            "username": "test_update",
            "email"   : "test_update",
            "password": "test_update",
        },
    )
    assert response.status_code == 401


def test_update_user(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "patate"}
    )
    login_response = client.post(
        "/login", data={"username": "chat", "password": "patate"}
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.put(
        "/user/update",
        json={"username": "chat", "email": "test_update", "password": "patate"},
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == 200

    response = client.get("/user/read_all")
    assert response.status_code == 200
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("username") == "chat"
    assert response.json()[0].get("email") == "test_update"
    assert response.json()[0].get("posts") == []


def test_delete_user(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "patate"}
    )
    login_response = client.post(
        "/login", data={"username": "chat", "password": "patate"}
    )
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.delete(
        "/user/delete", headers={"Authorization": f"bearer {access_token}"}
    )
    assert response.status_code == 204
