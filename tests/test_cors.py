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

    def test_disallowed_methods_headers(self):
        # OPTIONS request with disallowed method (e.g. GET/DELETE) should not allow DELETE
        response = self.client.options(
            "/parse",
            headers={
                "Origin": "https://luismarrero.me",
                "Access-Control-Request-Method": "DELETE",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        allowed_methods = response.headers.get("access-control-allow-methods", "")
        self.assertNotIn("DELETE", [m.strip() for m in allowed_methods.split(",")])

        # OPTIONS request with disallowed header (e.g. authorization) should not allow authorization
        response = self.client.options(
            "/parse",
            headers={
                "Origin": "https://luismarrero.me",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "authorization",
            },
        )
        allowed_headers = response.headers.get("access-control-allow-headers", "")
        self.assertNotIn("authorization", [h.strip().lower() for h in allowed_headers.split(",")])

    def test_input_max_length(self):
        # Payload size of 100,000 characters should be allowed
        valid_payload = "a" * 100000
        response = self.client.post("/parse", json={"text": valid_payload})
        self.assertEqual(response.status_code, 200)

        # Payload size > 100,000 characters should be rejected with 422
        invalid_payload = "a" * 100001
        response = self.client.post("/parse", json={"text": invalid_payload})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
