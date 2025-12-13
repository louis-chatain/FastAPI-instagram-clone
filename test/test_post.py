from fastapi.testclient import TestClient


def create_user(client: TestClient):
    client.post(
        "/user/create", json={"username": "chat", "email": "chat", "password": "patate"}
    )

    login_response = client.post(
        "/login", data={"username": "chat", "password": "patate"}
    )
    access_token = login_response.json()["access_token"]

    return access_token


def create_post(access_token, client: TestClient):
    response = client.post(
        "/post/create",
        json={"image_url": "test1", "image_url_type": "test2", "caption": "test3"},
        headers={"Authorization": f"bearer {access_token}"},
    )
    return response


def test_create_post(client: TestClient):
    access_token = create_user(client)

    response = create_post(access_token, client)
    assert response.status_code == 201


def test_read_current_user(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)

    response = client.get(
        "/post/read_current_user",
        headers={"Authorization": f"bearer {access_token}"}
    )

    assert response.status_code == 200
    response_value = response.json()[0]
    assert response_value.get("id") == 1
    assert response_value.get("image_url") == "test1"
    assert response_value.get("image_url_type") == "test2"
    assert response_value.get("caption") == "test3"
    assert response_value.get("timestamp") == "2025-12-13"
    user_info = response_value.get("users")
    assert user_info.get("id") == 1
    assert user_info.get("username") == "chat"
    assert user_info.get("email") == "chat"
    assert response_value.get("comments") == []


def test_read_all_post(client: TestClient):
    access_token = create_user(client)
    response = create_post(access_token, client)
    assert response.status_code == 201

    response = client.get("/post/read_all")
    response_value = response.json()[0]
    assert response.status_code == 200
    assert response_value.get("id") == 1
    assert response_value.get("image_url") == "test1"
    assert response_value.get("image_url_type") == "test2"
    assert response_value.get("caption") == "test3"
    assert response_value.get("timestamp") == "2025-12-13"
    user_info = response_value.get("users")
    assert user_info.get("id") == 1
    assert user_info.get("username") == "chat"
    assert user_info.get("email") == "chat"
    assert response_value.get("comments") == []


def test_update_post(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)

    response = client.put(
        "/post/update",
        params={"id": 1},
        json={
            "image_url": "update1",
            "image_url_type": "update2",
            "caption": "update3",
        },
        headers={"Authorization": f"bearer {access_token}"},
    )

    assert response.status_code == 200
    response = client.get("/post/read_all")
    response_value = response.json()[0]
    assert response.status_code == 200
    assert response_value.get("id") == 1
    assert response_value.get("image_url") == "update1"
    assert response_value.get("image_url_type") == "update2"
    assert response_value.get("caption") == "update3"
    assert response_value.get("timestamp") == "2025-12-13"
    user_info = response_value.get("users")
    assert user_info.get("id") == 1
    assert user_info.get("username") == "chat"
    assert user_info.get("email") == "chat"
    assert response_value.get("comments") == []


def test_delete_user(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)

    response = client.delete(
        "/post/delete",
        params={"id": 1},
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == 204
