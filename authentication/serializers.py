# authentication/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# -----------------------------
# JWT personalizado
# -----------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = user.user_type
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        return token

# -----------------------------
# Registro de usuários
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "user_type")
        read_only_fields = ("id",)

    def validate_user_type(self, value):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Usuário não autenticado.")

        creator = request.user

        # ADMIN pode criar qualquer tipo
        if creator.user_type == User.UserType.ADMIN:
            return value

        # EMPRESA pode criar AFILIADO e CLIENTE
        if creator.user_type == User.UserType.EMPRESA:
            if value not in [User.UserType.AFILIADO, User.UserType.CLIENTE]:
                raise serializers.ValidationError(
                    "Empresa só pode criar Afiliado ou Cliente."
                )
            return value

        # AFILIADO pode criar CLIENTE
        if creator.user_type == User.UserType.AFILIADO:
            if value != User.UserType.CLIENTE:
                raise serializers.ValidationError(
                    "Afiliado só pode criar Cliente."
                )
            return value

        raise serializers.ValidationError(
            "Este tipo de usuário não pode criar outros."
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        # created_by vem da view via perform_create
        user.save()
        return user

# -----------------------------
# Perfil do usuário logado
# -----------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "user_type",
            "is_active",
            "is_verified",
        )

# -----------------------------
# Serializer para listagens de usuários
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "user_type",
            "is_active",
            "is_verified",
        )