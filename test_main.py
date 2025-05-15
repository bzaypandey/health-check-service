from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Health Check Service!"}

def test_add_service():
    service = {
        "id": 1,
        "name": "Bijaya Pandey",
        "status": "healthy",
        "description": "Bijaya is in good health with no reported issues"
    }
    response = client.post("/health", json=service)
    assert response.status_code == 200
    assert response.json() == service

def test_get_all_services():
    response = client.get("/health")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_service():
    response = client.get("/health/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Bijaya Pandey"

def test_update_service():
    updated = {
        "id": 1,
        "name": "Bijaya Pandey",
        "status": "degraded",
        "description": "Bijaya is experiencing mild symptoms of fatigue"
    }
    response = client.put("/health/1", json=updated)
    assert response.status_code == 200
    assert response.json()["status"] == "degraded"

def test_delete_service():
    response = client.delete("/health/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_nonexistent_service():
    response = client.get("/health/999")
    assert response.status_code == 404

def test_add_duplicate_service():
    service = {
        "id": 2,
        "name": "Sandhya Giri",
        "status": "healthy",
        "description": "Sandhya is in excellent health and active"
    }
    client.post("/health", json=service)
    response = client.post("/health", json=service)
    assert response.status_code == 400
