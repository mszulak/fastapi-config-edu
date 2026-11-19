

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "ai-backend", "status": "online"}

def test_create_task_without_token_returns_401(client):
    response = client.post("/tasks/", json={"title": "Test", "estimated_hours": 5})
    assert response.status_code == 401
