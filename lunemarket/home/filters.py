import django.db.models
from django.template.defaulttags import register
from django.conf import settings


@register.filter
def get_categories_batches(categories: django.db.models.QuerySet):
    return [
        categories[listing: listing+settings.CATEGORIES_BATCH_SIZE]
        for listing in range(0, len(categories), settings.CATEGORIES_BATCH_SIZE)
    ]
