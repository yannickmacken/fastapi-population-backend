from fastapi.testclient import TestClient
import unittest

from main import app


client = TestClient(app)


class TestAPI(unittest.TestCase):
    """Test class for API. Post requests will write to development db."""

    # Setup
    sample_reading = {
        "value": 42.5
    }

    def test_submit_reading(self):
        response = client.post("/submit/", json=self.sample_reading)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue("id" in data)

    def test_get_all_readings(self):

        # Check length of readings
        response = client.get("/readings/")
        readings = response.json()
        response = client.get("/readings/")
        self.assertEqual(response.status_code, 200)
        original_len_readings = len(readings)

        # Submit a reading
        client.post("/submit/", json=self.sample_reading)

        # Now, get all readings and check if our submitted reading is present
        response = client.get("/readings/")
        self.assertEqual(response.status_code, 200)
        readings = response.json()
        self.assertEqual(len(readings), original_len_readings + 1)
