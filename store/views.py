from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.permissions import IsEmpresa

from .models import Store
from .serializers import StoreSerializer


# -----------------------------
# Paginação
# -----------------------------
class StorePagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


# -----------------------------
# Listar / pesquisar Stores
# -----------------------------
class CompanyStoreListView(generics.ListAPIView):
    """
    Lista todas as lojas pertencentes à empresa
    do usuário autenticado.

    Pesquisa:

        ?search=nome

    Paginação:

        ?limit=20&offset=0

    Ordenação:

        ?ordering=name
        ?ordering=-name
        ?ordering=created_at
        ?ordering=-created_at
    """

    serializer_class = StoreSerializer

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        permissions.IsAuthenticated,
        IsEmpresa
    ]

    pagination_class = StorePagination

    def get_queryset(self):
        company = self.request.user.owned_company

        queryset = Store.objects.filter(
            company=company
        )

        # -----------------------------
        # Pesquisa
        # -----------------------------
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search)
            )

        # -----------------------------
        # Ordenação
        # -----------------------------
        ordering = self.request.query_params.get(
            "ordering",
            "name"
        )

        allowed_ordering = {
            "name",
            "-name",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("name")

        return queryset


# -----------------------------
# Criar Store
# -----------------------------
class CompanyStoreCreateView(generics.CreateAPIView):
    """
    Permite que uma empresa crie uma nova loja.

    A empresa é determinada automaticamente através
    do usuário autenticado.

    O frontend NÃO envia company_id.
    """

    serializer_class = StoreSerializer

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        permissions.IsAuthenticated,
        IsEmpresa
    ]

    def perform_create(self, serializer):
        company = self.request.user.owned_company

        serializer.save(
            company=company
        )


# -----------------------------
# Editar Store
# -----------------------------
class CompanyStoreUpdateView(generics.UpdateAPIView):
    """
    Permite editar uma loja pertencente à empresa
    do usuário autenticado.

    PUT  -> atualização completa
    PATCH -> atualização parcial
    """

    serializer_class = StoreSerializer

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        permissions.IsAuthenticated,
        IsEmpresa
    ]

    lookup_field = "id"
    lookup_url_kwarg = "store_id"

    def get_queryset(self):
        company = self.request.user.owned_company

        return Store.objects.filter(
            company=company
        )


# -----------------------------
# Deletar Store
# -----------------------------
class CompanyStoreDeleteView(generics.DestroyAPIView):
    """
    Permite deletar uma loja pertencente à empresa
    do usuário autenticado.
    """

    serializer_class = StoreSerializer

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        permissions.IsAuthenticated,
        IsEmpresa
    ]

    lookup_field = "id"
    lookup_url_kwarg = "store_id"

    def get_queryset(self):
        company = self.request.user.owned_company

        return Store.objects.filter(
            company=company
        )