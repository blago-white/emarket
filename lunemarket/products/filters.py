import django.db.models
from django.template.defaulttags import register
from django.conf import settings
from django.db.models import Max


@register.filter
def get_categories_batches(categories: django.db.models.QuerySet):
    return [
        categories[listing: listing+settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE]
        for listing in range(0, len(categories), settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE)
    ]


@register.filter
def get_prices_range(max_item_price: float) -> list:
    max_item_price = float(max_item_price)
    price_range = list(range(0, int(max_item_price), 1000))

    if price_range[-1] < max_item_price:
        price_range.append(int(max_item_price))

    return price_range


@register.filter
def spaces_to_dashes(string: str) -> str:
    return string.replace(" ", "-") if string else string


@register.filter
def dashes_to_spaces(string: str) -> str:
    return string.replace("-", " ") if string else string


@register.filter
def get_url_arg_from_bool(value: bool, name: str) -> str:
    return name if value else ""


@register.filter
def invert_sorting(sorting: str) -> str:
    try:
        return str(int(not bool(int(sorting))))
    except:
        return sorting


def compile_url_args_for_pagination(price: str = None, filters: int = None, min_: int = None) -> str:
    url_args = str()

    for name, value in (("price", price), ("filters", filters), ("min", min_)):
        url_args += f"&{name}={value}" if value is not None else ""

    return url_args


def get_ordering_field_from_url_arg(url_arg: str, field: str) -> str:
    try:
        return field if not int(url_arg) else "-" + field
    except:
        return field


def get_url_arg_from_ordering_field(field: str) -> int:
    return int(field.startswith("-"))

