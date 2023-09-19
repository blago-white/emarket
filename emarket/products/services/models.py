from django.db.models import Model


def get_max_product_price(products: Model, price_field: str) -> float:
    return products.objects.all().aggregate(Max(price_field))[f"{price_field}__max"]
