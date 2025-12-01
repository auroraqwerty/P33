import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestClassesAPI:
    def test_get_classes(self):
        response = client.get("/api/v1/classes")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "classes" in data["data"]

    def test_create_class(self):
        new_class_data = {"name": "Test Class"}
        response = client.post("/api/v1/classes", json=new_class_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["message"] == "Class created successfully"
        assert data["data"]["class"]["name"] == "Test Class"

    def test_create_class_empty_name(self):
        response = client.post("/api/v1/classes", json={"name": ""})
        assert response.status_code == 400

    def test_update_class(self):
        # First create a class
        create_response = client.post("/api/v1/classes", json={"name": "To Update"})
        class_id = create_response.json()["data"]["class"]["id"]

        # Then update it
        update_data = {"new_name": "Updated Class"}
        response = client.put(f"/api/v1/classes/{class_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["class"]["name"] == "Updated Class"

    def test_update_nonexistent_class(self):
        response = client.put("/api/v1/classes/999", json={"new_name": "Test"})
        assert response.status_code == 404

    def test_delete_class(self):
        # First create a class
        create_response = client.post("/api/v1/classes", json={"name": "To Delete"})
        class_id = create_response.json()["data"]["class"]["id"]

        response = client.delete(f"/api/v1/classes/{class_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True

    def test_delete_nonexistent_class(self):
        response = client.delete("/api/v1/classes/999")
        assert response.status_code == 404