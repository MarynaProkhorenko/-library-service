from django.db import models

from borrowing_service.models import Borrowing


class Payment(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = "Pending"
        PAID = "Paid"

    class TypeChoice(models.TextChoices):
        PAYMENT = "Payment"
        FINE = "Fine"

    status = models.CharField(max_length=8, choices=StatusChoice.choices)
    type = models.CharField(max_length=7, choices=TypeChoice.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=255, unique=True)
    money_to_pay = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["money_to_pay"]

    def __str__(self) -> str:
        return (
            f"Session id: {self.session_id} "
            f"money to pay: {self.money_to_pay} USD"
        )
