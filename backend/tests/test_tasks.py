import pytest

from app.core.config import settings

def test_create_and_read_task(client, mock_celery_delay):
    response = client.post("/tasks/?token=token_test", json={"title": "Test", "estimated_hours": 10})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert "internal_worker_note" not in data
    mock_celery_delay.assert_called_once_with(data["id"])

    response = client.get(f"/tasks/{data['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test"
    assert response.json()["description"] == None

@pytest.mark.parametrize("invalid_hours", [0, -5, settings.max_hours_limit + 1])
def test_create_task_invalid_hours_returns_400(client, invalid_hours):
    response = client.post("/tasks/?token=token_test", json={"title": "Test-0", "estimated_hours": invalid_hours})
    assert response.status_code == 400

def test_update_task_ignores_status_change(client):
    create_response = client.post("/tasks/?token=token_test", json={"title": "Test", "estimated_hours": 10})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/tasks/{task_id}?token=token_test",
        json={"title": "New Test", "status": "completed"},
    )
    assert patch_response.status_code == 200
    data = patch_response.json()

    assert data["title"] == "New Test"
    assert data["status"] == "pending"