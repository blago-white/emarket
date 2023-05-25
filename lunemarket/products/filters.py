import django.db.models
from django.template.defaulttags import register
from django.conf import settings


@register.filter
def get_categories_batches(categories: django.db.models.QuerySet):
    return [
        categories[listing: listing+settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE]
        for listing in range(0, len(categories), settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE)
    ]


@register.filter
def spaces_to_dashes(string: str) -> str:
    return string.replace(" ", "-") if string else string


@register.filter
def dashes_to_spaces(string: str) -> str:
    return string.replace("-", " ") if string else string
