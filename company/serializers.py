from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "cnpj",
            "owner",
            "owner_email",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["owner", "created_at"]