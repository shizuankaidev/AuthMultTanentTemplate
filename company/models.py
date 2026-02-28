# company/models.py

from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    cnpj = models.CharField(max_length=18, unique=True, null=False, default="00000000/0001-00")  # ⚡ default temporário
    
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_company",
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name