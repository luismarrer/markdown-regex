import unittest
from fastapi.testclient import TestClient
from main import app

class TestCORS(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_allowed_origins(self):
        allowed_origins = [
            "https://luismarrero-me.localhost:1355",
            "https://luismarrero.me",
            "https://www.luismarrero.me",
        ]
        for origin in allowed_origins:
            response = self.client.options(
                "/parse",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type",
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers.get("access-control-allow-origin"), origin)

    def test_disallowed_origins(self):
        disallowed_origins = [
            "http://luismarrero.me",
            "https://evil.com",
            "https://luismarrero.me.evil.com",
            "https://localhost:1355",
        ]
        for origin in disallowed_origins:
            response = self.client.options(
                "/parse",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type",
                },
            )
            # Under FastAPI's CORSMiddleware, disallowed origins either fail with 400
            # or do not return the 'access-control-allow-origin' header.
            self.assertEqual(response.status_code, 400)
            self.assertNotIn("access-control-allow-origin", response.headers)

if __name__ == "__main__":
    unittest.main()
