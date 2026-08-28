# store/models.py

from django.db import models


class Store(models.Model):
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.CASCADE,
        related_name="stores"
    )

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "slug"],
                name="unique_store_slug_per_company"
            )
        ]

        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.company.name}"