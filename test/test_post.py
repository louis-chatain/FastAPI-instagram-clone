from fastapi.testclient import TestClient


def test_create_post(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "patate"}
    )

    login_response = client.post(
        "/login", data={"username": "chat", "password": "patate"}
    )
    access_token = login_response.json()["access_token"]

    response = client.post(
        "/post/create",
        json={"image_url": "string", "image_url_type": "string", "caption": "string"},
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == 201

def test_read_post(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "patate"}
    )

    login_response = client.post(
        "/login", data={"username": "chat", "password": "patate"}
    )
    access_token = login_response.json()["access_token"]

    response = client.post(
        "/post/create",
        json={"image_url": "test1", "image_url_type": "test2", "caption": "le caption quoi"},
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == 201

    response = client.get("/post/read_all")
    response_value = response.json()[0]
    assert response.status_code == 200
    assert response_value.get("id") == 1
    assert response_value.get("image_url") == "test1"
    assert response_value.get("image_url_type") == "test2"
    assert response_value.get("caption") == "le caption quoi"
    assert response_value.get("timestamp") == "2025-12-12"
    user_info = response_value.get("users")
    assert user_info.get("id") == 1
    assert user_info.get("username") == "chat"
    assert user_info.get("email") == "chat"

    assert response_value.get("comments") == []
