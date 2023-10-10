from django.db import models


def get_max_product_price(products: models.Model, price_field_name: str) -> float:
    return products.objects.all().aggregate(models.Max(price_field_name))[f"{price_field_name}__max"]
