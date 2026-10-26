from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("akash", password="Pass12345!")

    def test_login_valid(self):
        r = self.client.post("/api/auth/login/", {"username": "akash", "password": "Pass12345!"})
        self.assertEqual(r.status_code, 200)

    def test_login_invalid(self):
        r = self.client.post("/api/auth/login/", {"username": "akash", "password": "wrong"})
        self.assertEqual(r.status_code, 400)

    def test_protected_requires_auth(self):
        self.assertIn(self.client.get("/api/auth/me/").status_code, (401, 403))

    def test_logout(self):
        self.client.login(username="akash", password="Pass12345!")
        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)
