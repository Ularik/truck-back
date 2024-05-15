from django.test import TestCase
from ninja.testing import TestClient
from .views import router


class HelloTest(TestCase):
    def test_hello(self):
        client = TestClient(router)
        response = client.get("/list")

        self.assertEqual(response.status_code, 200)