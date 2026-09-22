import os
import sys
import unittest
from fastapi.testclient import TestClient

# Add src/engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "engine"))
from main import app

class TestEngineService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("service"), "oveRthinkLM-Engine")
        self.assertEqual(data.get("status"), "operational")
        self.assertIn("Depth-0 (Vanilla LLM)", data.get("configurations", []))

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("uptime_seconds", data)
        self.assertEqual(data.get("sandbox_isolation"), "process-level")

    def test_status_endpoint(self):
        response = self.client.get("/v1/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("service"), "oveRthinkLM-Engine")
        self.assertEqual(data.get("engine_state"), "ready")
        self.assertIn("redis_state_store", data)

    def test_repl_execute_endpoint(self):
        payload = {
            "code": "result = 2 + 2",
            "timeout_seconds": 5,
            "context_variables": {"x": 10}
        }
        response = self.client.post("/v1/repl/execute", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIn("REPL", data.get("stdout"))
        self.assertGreaterEqual(data.get("duration_ms"), 0.0)

if __name__ == "__main__":
    unittest.main()
