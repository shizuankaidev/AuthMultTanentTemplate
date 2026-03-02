from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Company

User = get_user_model()


class CompanyAdminTests(APITestCase):

    def setUp(self):
        # =========================
        # USERS
        # =========================

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@email.com",
            password="admin123",
            user_type=User.UserType.ADMIN
        )

        self.user_empresa = User.objects.create_user(
            username="empresa",
            email="empresa@email.com",
            password="empresa123",
            user_type=User.UserType.EMPRESA
        )

        self.user_empresa2 = User.objects.create_user(
            username="empresa2",
            email="empresa2@email.com",
            password="empresa123",
            user_type=User.UserType.EMPRESA
        )

        # =========================
        # AUTH JWT
        # =========================

        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        # =========================
        # COMPANY BASE
        # =========================

        self.company = Company.objects.create(
            name="Empresa Teste",
            slug="empresa-teste",
            cnpj="12.345.678/0001-99"
        )

    # =====================================================
    # CRUD
    # =====================================================

    def test_create_company(self):
        url = reverse("company-list")

        data = {
            "name": "Nova Empresa",
            "slug": "nova-empresa",
            "cnpj": "11.111.111/0001-11"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)

    def test_delete_company(self):
        url = reverse("company-detail", args=[self.company.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    # =====================================================
    # OWNER
    # =====================================================

    def test_set_owner_success(self):
        url = reverse("company-owner", args=[self.company.id])

        response = self.client.post(url, {
            "user_id": self.user_empresa.id
        })

        self.company.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.company.owner, self.user_empresa)

    def test_set_owner_invalid_user_type(self):
        url = reverse("company-owner", args=[self.company.id])

        response = self.client.post(url, {
            "user_id": self.admin.id  # ADMIN não pode ser owner
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_owner_already_owner_of_other_company(self):
        Company.objects.create(
            name="Empresa 2",
            slug="empresa-2",
            cnpj="22.222.222/0001-22",
            owner=self.user_empresa
        )

        url = reverse("company-owner", args=[self.company.id])

        response = self.client.post(url, {
            "user_id": self.user_empresa.id
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_revoke_owner_success(self):
        self.company.owner = self.user_empresa
        self.company.save()

        url = reverse("company-owner", args=[self.company.id])

        response = self.client.delete(url)

        self.company.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(self.company.owner)

    def test_revoke_owner_without_owner(self):
        url = reverse("company-owner", args=[self.company.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =====================================================
    # PERMISSION
    # =====================================================

    def test_non_admin_cannot_access(self):
        user = User.objects.create_user(
            username="usercomum",
            email="user@email.com",
            password="123456",
            user_type=User.UserType.EMPRESA
        )

        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        url = reverse("company-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)