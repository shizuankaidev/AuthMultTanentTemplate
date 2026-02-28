from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):

    class UserType(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPRESA = "EMPRESA", "Empresa"
        AFILIADO = "AFILIADO", "Afiliado"
        CLIENTE = "CLIENTE", "Cliente"

    email = models.EmailField(unique=True)

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENTE
    )

    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users"
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def clean(self):
        if not self.created_by:
            return

        creator = self.created_by

        if creator.user_type == self.UserType.ADMIN:
            return

        if creator.user_type == self.UserType.EMPRESA:
            if self.user_type not in [self.UserType.AFILIADO, self.UserType.CLIENTE]:
                raise ValidationError("Empresa só pode criar Afiliado ou Cliente.")

        elif creator.user_type == self.UserType.AFILIADO:
            if self.user_type != self.UserType.CLIENTE:
                raise ValidationError("Afiliado só pode criar Cliente.")

        else:
            raise ValidationError("Este tipo de usuário não pode criar outros.")

    def save(self, *args, **kwargs):
        self.full_clean()  # 🔥 força validação sempre
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.user_type})"