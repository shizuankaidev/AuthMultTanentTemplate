from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from authentication.permissions import IsAdmin
from authentication.models import User
from .models import Company
from .serializers import CompanySerializer


class CompanyAdminViewSet(ModelViewSet):
    """
    CRUD completo para gerenciamento de Companies.
    Apenas usuários Admin ou superuser podem acessar.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [JWTAuthentication]  # ⚡ obrigatório para JWT
    permission_classes = [IsAuthenticated, IsAdmin]

    # =========================
    # OWNER (SUB-RESOURCE)
    # =========================

    @action(detail=True, methods=["post"], url_path="owner")
    def set_owner(self, request, pk=None):
        """
        Define um usuário do tipo EMPRESA como owner da company.
        Admin master pode atribuir qualquer usuário do tipo EMPRESA.
        """
        company = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"detail": "user_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)

        if user.user_type != User.UserType.EMPRESA:
            return Response({"detail": "Apenas usuários do tipo EMPRESA podem ser owner."}, status=status.HTTP_400_BAD_REQUEST)

        # remove esta linha:
        # if getattr(user, "company_id", None) != company.id:
        #     return Response({"detail": "Usuário não pertence a esta empresa."}, status=status.HTTP_400_BAD_REQUEST)

        if getattr(user, "owned_company", None) and user.owned_company != company:
            return Response({"detail": "Usuário já é owner de outra empresa."}, status=status.HTTP_400_BAD_REQUEST)

        company.owner = user
        company.save(update_fields=["owner"])

        return Response({"detail": "Owner definido com sucesso."}, status=status.HTTP_200_OK)
    
    
    @set_owner.mapping.delete
    def revoke_owner(self, request, pk=None):
        """
        Remove o owner da company.
        """
        company = self.get_object()

        if not company.owner:
            return Response({"detail": "Empresa não possui owner definido."}, status=status.HTTP_400_BAD_REQUEST)

        company.owner = None
        company.save(update_fields=["owner"])

        return Response({"detail": "Owner removido com sucesso."}, status=status.HTTP_200_OK)