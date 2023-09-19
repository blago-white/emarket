from django.db import models as django_models

from products.models import models


def get_main_categories() -> django_models.QuerySet:
    return models.Category.objects.filter(parent=None)


def get_categories_queryset(parent_category: str | models.Category,
                            ordering: str,
                            **query_filters) -> django_models.QuerySet:
    return models.Category.objects.filter(parent=parent_category).values("title").annotate(
        price=django_models.Avg(django_models.F("phone__price")),
        photo=django_models.Max(django_models.F("phone__photo")),
        _count_items_in=django_models.Sum("phone__products_count")
    ).filter(**query_filters, _count_items_in__gt=0).annotate(
        count_products_in=django_models.Count("phone")
    ).order_by(ordering or "-price")
