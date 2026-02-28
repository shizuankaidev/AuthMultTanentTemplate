from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseUserTypePermission(BasePermission):
    allowed_types = []

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.user_type in self.allowed_types


class IsAdmin(BaseUserTypePermission):
    allowed_types = [User.UserType.ADMIN]

    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.is_superuser


class IsEmpresa(BaseUserTypePermission):
    allowed_types = [User.UserType.EMPRESA]


class IsAfiliado(BaseUserTypePermission):
    allowed_types = [User.UserType.AFILIADO]


class IsCliente(BaseUserTypePermission):
    allowed_types = [User.UserType.CLIENTE]