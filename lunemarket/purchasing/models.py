from typing import Union
from django.db import models
from products import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from products.models.models import Phones

__all__ = ["ShoppingBasket"]


class ShoppingBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=False)
    product = models.ForeignKey(Phones, on_delete=models.CASCADE, null=False, unique=False, default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ShoppingBasket"
        verbose_name_plural = "ShoppingBasket"
        unique_together = ("user", "product")
