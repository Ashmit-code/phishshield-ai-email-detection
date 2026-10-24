"""
Integration tests for FastAPI server endpoints.
"""
import unittest
from fastapi.testclient import TestClient
from server import app

class TestServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_api_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "phishshield-ai")

    def test_api_status(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("models_loaded", data)
        self.assertIn("dataset_stats", data)

    def test_api_samples(self):
        response = self.client.get("/api/samples")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("samples", data)
        self.assertGreater(len(data["samples"]), 0)

    def test_api_analyze_valid(self):
        payload = {
            "text": "Action required: Verify your Apple ID immediately at http://10.0.0.1/auth",
            "sender": "noreply@apple-security-check.com",
            "subject": "Security Alert"
        }
        response = self.client.post("/api/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("verdict", data)
        self.assertIn("risk_score", data)
        self.assertIn("threat_level", data)
        self.assertIn("features", data)

    def test_api_analyze_empty(self):
        response = self.client.post("/api/analyze", json={"text": "   "})
        self.assertEqual(response.status_code, 400)

    def test_api_metrics(self):
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dataset_stats", data)
        self.assertIn("benchmarks", data)

    def test_static_frontend_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<!DOCTYPE html>", response.text)

if __name__ == "__main__":
    unittest.main()
