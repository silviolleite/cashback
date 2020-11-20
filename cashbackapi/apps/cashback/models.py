import logging

from django.contrib.auth.models import User
from django.db import models
from . import validators
from .managers import CashbackManager

logger = logging.getLogger(__name__)

APPROVED = "A"
MODERATE = "M"

STATUS_CHOICES = ((APPROVED, "Aprovado"), (MODERATE, "Em Validação"))

SPECIAL_SELLER_DOCUMENT = "15350946056"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document = models.CharField(max_length=11, validators=[validators.validate_cpf],  unique=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=MODERATE)
    created_at = models.DateField(auto_now=True)

    objects = models.Manager()
    cashback_total = CashbackManager()

    def save(self, *args, **kwargs):
        if self._is_special_seller():
            self.status = "A"
        super().save(*args, **kwargs)

    def _is_special_seller(self):
        logging.info("Checking if is a special seller")
        if self.seller.document == SPECIAL_SELLER_DOCUMENT:
            return True
        return False

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.code
