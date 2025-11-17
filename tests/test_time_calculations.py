import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestTimeCalculationsAPI:
    def test_calculate_time_until_exit_valid(self):
        # Test with a time 2 hours from now
        future_time = datetime.now() + timedelta(hours=2)
        time_data = {
            "exit_hour": future_time.hour,
            "exit_minute": future_time.minute
        }
        response = client.post("/api/v1/time-until-exit", json=time_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "time_until_exit" in data["data"]
        # Should be approximately 2 hours (allowing some tolerance)
        assert 1 <= data["data"]["time_until_exit"]["hours"] <= 2.1

    def test_calculate_time_until_exit_tomorrow(self):
        # Test with a time that's earlier than current time (should calculate for tomorrow)
        time_data = {
            "exit_hour": 8,  # 8 AM
            "exit_minute": 0
        }
        response = client.post("/api/v1/time-until-exit", json=time_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # Should be more than 12 hours (overnight)
        assert data["data"]["time_until_exit"]["hours"] >= 12

    def test_calculate_time_until_exit_invalid_hour(self):
        time_data = {
            "exit_hour": 25,  # Invalid hour
            "exit_minute": 0
        }
        response = client.post("/api/v1/time-until-exit", json=time_data)
        assert response.status_code == 422  # Validation error

    def test_calculate_time_until_exit_invalid_minute(self):
        time_data = {
            "exit_hour": 12,
            "exit_minute": 60  # Invalid minute
        }
        response = client.post("/api/v1/time-until-exit", json=time_data)
        assert response.status_code == 422  # Validation error

    def test_calculate_time_until_exit_negative_values(self):
        time_data = {
            "exit_hour": -1,  # Invalid negative hour
            "exit_minute": -5  # Invalid negative minute
        }
        response = client.post("/api/v1/time-until-exit", json=time_data)
        assert response.status_code == 422  # Validation error