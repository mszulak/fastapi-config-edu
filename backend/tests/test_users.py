def test_create_user_with_task(client):
    response = client.post(
        "/users/?token=token_test",
        json={"email": "test@email.com", "full_name": "Test Full Name"},
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    response = client.post(
        "/tasks/?token=token_test",
        json={"title": "Test", "estimated_hours": 10, "user_id": user_id},
    )
    assert response.status_code == 201

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"][0]["user_id"] == user_id
    assert data["tasks"][0]["title"] == "Test"
    assert data["tasks"][0]["estimated_hours"] == 10


def test_create_duplicate_user_email_returns_409(client):
    response = client.post(
        "/users/?token=token_test",
        json={"email": "test@email.com", "full_name": "Test Full Name"},
    )

    response = client.post(
        "/users/?token=token_test",
        json={"email": "test@email.com", "full_name": "New Test Full Name"},
    )

    assert response.status_code == 409


def test_create_task_with_nonexistent_user_returns_404(client):
    response = client.post(
        "/tasks/?token=token_test",
        json={"title": "Test", "estimated_hours": 10, "user_id": 1},
    )
    assert response.status_code == 404
