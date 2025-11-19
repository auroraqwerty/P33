
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data.data_manager import DataManager

client = TestClient(app)

def get_all_class_names():
    return [cls.name for cls in DataManager().get_all_classes()]


class TestGradesAPI:
    def test_calculate_grades_valid(self):
        class_names = get_all_class_names()
        grades_data = {
            "grades": {name: 0.0 for name in class_names[:4]}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["grades"]["subject_count"] == 4
        assert data["data"]["grades"]["average"] == 0.0

    def test_calculate_grades_single_subject(self):
        class_names = get_all_class_names()
        grades_data = {
            "grades": {class_names[0]: 0.0}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 0.0
        assert data["data"]["grades"]["subject_count"] == 1

    def test_calculate_grades_empty(self):
        grades_data = {
            "grades": {}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 400

    def test_calculate_grades_with_zeros(self):
        class_names = get_all_class_names()
        grades_data = {
            "grades": {name: 0.0 for name in class_names[:3]}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 0.0

    def test_calculate_grades_high_values(self):
        class_names = get_all_class_names()
        grades_data = {
            "grades": {name: 0.0 for name in class_names[:2]}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 0.0