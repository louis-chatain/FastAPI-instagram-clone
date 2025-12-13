from fastapi.testclient import TestClient
from test_post import create_user, create_post


def create_comment(access_token, client: TestClient):
    response = client.post(
        "/comment/create",
        json={"text": "create1", "post_id": 1},
        headers={"Authorization": f"bearer {access_token}"},
    )
    return response


def test_create_comment(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)

    response = client.post(
        "/comment/create",
        json={"text": "create1", "post_id": 1},
        headers={"Authorization": f"bearer {access_token}"},
    )

    assert response.status_code == 201


def test_read_all(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)
    create_comment(access_token, client)

    response = client.get(
        "/comment/read_all", headers={"Authorization": f"bearer {access_token}"}
    )

    assert response.status_code == 200
    comment_response = response.json()[0]
    assert comment_response.get("id") == 1
    assert comment_response.get("text") == "create1"
    assert comment_response.get("timestamp") == "2025-12-13"
    assert comment_response.get("user_id") == 1
    post_info = comment_response.get("post")
    assert post_info.get("id") == 1
    assert post_info.get("image_url") == "test1"
    assert post_info.get("image_url_type") == "test2"
    assert post_info.get("caption") == "test3"
    assert post_info.get("timestamp") == "2025-12-13"


def test_update_comment(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)
    create_comment(access_token, client)

    response = client.put(
        "/comment/update",
        json={"id": 1, "text": "update1"},
        headers={"Authorization": f"bearer {access_token}"},
    )
    assert response.status_code == 200

    response = client.get(
        "/comment/read_all", headers={"Authorization": f"bearer {access_token}"}
    )
    assert response.status_code == 200
    comment_response = response.json()[0]
    assert comment_response.get("id") == 1
    assert comment_response.get("text") == "update1"
    assert comment_response.get("timestamp") == "2025-12-13"
    assert comment_response.get("user_id") == 1
    post_info = comment_response.get("post")
    assert post_info.get("id") == 1
    assert post_info.get("image_url") == "test1"
    assert post_info.get("image_url_type") == "test2"
    assert post_info.get("caption") == "test3"
    assert post_info.get("timestamp") == "2025-12-13"


def test_delete_comment(client: TestClient):
    access_token = create_user(client)
    create_post(access_token, client)
    create_comment(access_token, client)

    response = client.delete(
        "/comment/delete",
        params={"id": 1},
        headers={"Authorization": f"bearer {access_token}"},
    )

    assert response.status_code == 204