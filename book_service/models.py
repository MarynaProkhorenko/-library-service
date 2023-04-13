from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverChoice(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverChoice.choices)
    inventory = models.ImageField(
        validators=MinValueValidator(0),
        default=0,
    )
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} {self.author}"


