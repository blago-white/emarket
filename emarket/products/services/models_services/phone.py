from emarket import config
from django.db import models as django_models

from products.models import models


def get_phones_queryset(category: models.Category, ordering: str, **query_filters) -> django_models.QuerySet:
    return models.Phone.objects.filter(category=category, products_count__gt=0, **query_filters).order_by(ordering)


def get_max_phone_price() -> float:
    max_phone_price = (models.Phone.objects.all().aggregate(django_models.Max('price'))["price__max"] or
                       config.MAX_PRODUCT_PRICE_USD)

    if max_phone_price < 5000:
        max_phone_price += 1

    return max_phone_price
