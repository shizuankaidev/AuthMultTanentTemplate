# authentication/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    UserSerializer,
)
from .permissions import IsAdmin

User = get_user_model()

# -----------------------------
# Paginação segura (limit + max limit)
# -----------------------------
class SafeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

# -----------------------------
# JWT Views
# -----------------------------
class LoginView(TokenObtainPairView):
    """
    Login usando JWT.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class RefreshView(TokenRefreshView):
    """
    Refresh do JWT.
    """
    permission_classes = [permissions.AllowAny]

# -----------------------------
# Registro de usuário (Admin)
# -----------------------------
class RegisterView(generics.CreateAPIView):
    """
    Registro de usuários feito apenas por Admin.
    Se não enviar `user_type`, será CLIENTE por padrão.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        user_type = self.request.data.get("user_type", User.UserType.CLIENTE)

        # Valida tipo de usuário
        if user_type not in User.UserType.values:
            raise serializers.ValidationError(
                {"user_type": f"Tipo de usuário inválido: {user_type}"}
            )

        serializer.save(created_by=self.request.user, user_type=user_type)

# -----------------------------
# Perfil do usuário logado
# -----------------------------
class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

# -----------------------------
# Listagem de usuários paginada (Admin)
# -----------------------------
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = SafeLimitOffsetPagination