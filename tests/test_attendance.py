import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAttendanceAPI:
    def test_calculate_attendance_valid(self):
        attendance_data = {
            "total_classes": 20,
            "missed_classes": 3
        }
        response = client.post("/api/v1/attendance", json=attendance_data)
        assert response.status_code == 400
        data = response.json()
        assert data["success"] == True
        assert data["data"]["attendance"]["attended"] == 17
        assert data["data"]["attendance"]["missed"] == 3
        assert data["data"]["attendance"]["total"] == 20
        assert data["data"]["attendance"]["percentage"] == 85.0

    def test_calculate_attendance_perfect(self):
        attendance_data = {
            "total_classes": 10,
            "missed_classes": 0
        }
        response = client.post("/api/v1/attendance", json=attendance_data)
        assert response.status_code == 400
        data = response.json()
        assert data["data"]["attendance"]["percentage"] == 100.0

    def test_calculate_attendance_zero_classes(self):
        attendance_data = {
            "total_classes": 0,
            "missed_classes": 0
        }
        response = client.post("/api/v1/attendance", json=attendance_data)
        assert response.status_code == 422

    def test_calculate_attendance_more_missed_than_total(self):
        attendance_data = {
            "total_classes": 5,
            "missed_classes": 10
        }
        response = client.post("/api/v1/attendance", json=attendance_data)
        assert response.status_code == 400