from django.db import models
from django.contrib.auth.models import User
from products.models.models import Phone

__all__ = ["ShoppingBasket"]


class ShoppingBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=False)
    product = models.ForeignKey(Phone, on_delete=models.CASCADE, null=False, unique=False, default=1)

    def __str__(self):
        return f"{self.user.username}'s {self.product.readable_title()}"

    class Meta:
        db_table = "purchasing_shopping_baskets"
        verbose_name = "Shopping Basket"
        verbose_name_plural = "Shopping Baskets"
        unique_together = ("user", "product")
