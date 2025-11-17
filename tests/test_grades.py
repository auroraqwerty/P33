import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestGradesAPI:
    def test_calculate_grades_valid(self):
        grades_data = {
            "grades": {
                "Math": 85.5,
                "Science": 92.0,
                "History": 78.0,
                "English": 88.5
            }
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["grades"]["subject_count"] == 4
        assert data["data"]["grades"]["average"] == 86.0

    def test_calculate_grades_single_subject(self):
        grades_data = {
            "grades": {
                "Math": 95.0
            }
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 95.0
        assert data["data"]["grades"]["subject_count"] == 1

    def test_calculate_grades_empty(self):
        grades_data = {
            "grades": {}
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 400

    def test_calculate_grades_with_zeros(self):
        grades_data = {
            "grades": {
                "Math": 0.0,
                "Science": 0.0,
                "History": 0.0
            }
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 0.0

    def test_calculate_grades_high_values(self):
        grades_data = {
            "grades": {
                "Math": 150.0,  # Above 100%
                "Science": 200.0
            }
        }
        response = client.post("/api/v1/grades", json=grades_data)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["grades"]["average"] == 175.0