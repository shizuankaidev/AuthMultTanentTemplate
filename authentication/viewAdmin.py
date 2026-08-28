from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAdmin
from .serializers import UserSerializer


User = get_user_model()


# -----------------------------
# Paginação segura
# -----------------------------
class AdminUserPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


# -----------------------------
# Listagem / pesquisa de usuários
# -----------------------------
class AdminUserListView(generics.ListAPIView):
    """
    Lista usuários para o painel administrativo.

    Suporta:

    ?limit=20
    ?offset=0

    Pesquisa:
    ?search=joao
    ?search=email@email.com
    ?search=123

    Filtros:
    ?user_type=EMPRESA
    ?is_active=true

    Ordenação:
    ?ordering=created_at
    ?ordering=-created_at
    ?ordering=email
    ?ordering=-email
    """

    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]

    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin
    ]

    pagination_class = AdminUserPagination

    def get_queryset(self):
        queryset = User.objects.all()

        # -----------------------------
        # Pesquisa
        # -----------------------------
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(id__icontains=search)
            )

        # -----------------------------
        # Filtro por tipo
        # -----------------------------
        user_type = self.request.query_params.get("user_type")

        if user_type:
            queryset = queryset.filter(
                user_type=user_type
            )

        # -----------------------------
        # Filtro por status
        # -----------------------------
        is_active = self.request.query_params.get("is_active")

        if is_active is not None:

            if is_active.lower() == "true":
                queryset = queryset.filter(
                    is_active=True
                )

            elif is_active.lower() == "false":
                queryset = queryset.filter(
                    is_active=False
                )

        # -----------------------------
        # Ordenação
        # -----------------------------
        ordering = self.request.query_params.get(
            "ordering",
            "-created_at"
        )

        allowed_ordering = {
            "id",
            "-id",
            "username",
            "-username",
            "email",
            "-email",
            "first_name",
            "-first_name",
            "last_name",
            "-last_name",
            "created_at",
            "-created_at",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset


# -----------------------------
# Atualização de usuário
# -----------------------------
class AdminUserUpdateView(generics.UpdateAPIView):
    """
    Permite que um Admin altere um usuário.

    PUT:
        Atualização completa.

    PATCH:
        Atualização parcial.

    Usuário identificado pelo ID.
    """

    queryset = User.objects.all()

    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]

    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin
    ]

    lookup_field = "id"
    lookup_url_kwarg = "user_id"