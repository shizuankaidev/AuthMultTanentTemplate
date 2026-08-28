from rest_framework import serializers

from .models import Store


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store

        fields = [
            "id",
            "company",
            "name",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "company",
            "created_at",
            "updated_at",
        ]

    def validate_slug(self, value):
        company = self.context["request"].user.owned_company

        queryset = Store.objects.filter(
            company=company,
            slug=value
        )

        # Durante edição, não considerar a própria loja
        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Já existe uma loja com este slug na sua empresa."
            )

        return value