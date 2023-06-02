from typing import Union
from django.db import models
from products import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from products.models.models import Cards


class ShoppingBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, unique=False)
    product = models.ForeignKey(Cards, on_delete=models.DO_NOTHING, null=False, unique=False)

    def __str__(self):
        return str(self.id)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        return super(ShoppingBasket, self).save(force_insert=force_insert,
                                                force_update=force_update,
                                                using=using,
                                                update_fields=update_fields)

    class Meta:
        verbose_name = "ShoppingBasket"
        verbose_name_plural = "ShoppingBasket"
        unique_together = ("user", "product")


def _product_is_unique_for_user(user: User, product: Cards):
    return not len(ShoppingBasket.objects.filter(user=user, product=product))
