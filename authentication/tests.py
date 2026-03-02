from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.login_url = reverse("login")
        self.refresh_url = reverse("refresh")
        self.profile_url = reverse("profile")
        self.register_url = reverse("register")

        # Admin
        self.admin = User.objects.create_user(
            email="admin@email.com",
            username="admin",
            password="admin123",
            user_type=User.UserType.ADMIN,
            is_verified=True
        )

        # Usuário comum
        self.user = User.objects.create_user(
            email="user@email.com",
            username="user",
            password="user123",
            user_type=User.UserType.CLIENTE,
            is_verified=True
        )

    def authenticate(self, email, password):
        response = self.client.post(self.login_url, {
            "email": email,
            "password": password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )
        return response.data

    # ---------------------------
    # LOGIN
    # ---------------------------
    def test_login_returns_access_and_refresh(self):
        response = self.client.post(self.login_url, {
            "email": "admin@email.com",
            "password": "admin123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # ---------------------------
    # REFRESH
    # ---------------------------
    def test_refresh_token_returns_new_access(self):
        login_data = self.authenticate("admin@email.com", "admin123")

        response = self.client.post(self.refresh_url, {
            "refresh": login_data["refresh"]
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # ---------------------------
    # PROFILE
    # ---------------------------
    def test_profile_returns_logged_user(self):
        self.authenticate("admin@email.com", "admin123")

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "admin@email.com")

    # ---------------------------
    # REGISTER (ADMIN)
    # ---------------------------
    def test_admin_can_register(self):
        self.authenticate("admin@email.com", "admin123")

        response = self.client.post(self.register_url, {
            "email": "novo@email.com",
            "username": "novo",
            "password": "123456",
            "user_type": User.UserType.CLIENTE
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ---------------------------
    # REGISTER (NÃO ADMIN)
    # ---------------------------
    def test_non_admin_cannot_register(self):
        self.authenticate("user@email.com", "user123")

        response = self.client.post(self.register_url, {
            "email": "fail@email.com",
            "username": "fail",
            "password": "123456",
            "user_type": User.UserType.CLIENTE
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------------
    # USER TYPE INVÁLIDO
    # ---------------------------
    def test_invalid_user_type_returns_400(self):
        self.authenticate("admin@email.com", "admin123")

        response = self.client.post(self.register_url, {
            "email": "bad@email.com",
            "username": "bad",
            "password": "123456",
            "user_type": "INVALIDO"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)