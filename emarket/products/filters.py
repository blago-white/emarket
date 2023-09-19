from typing import Iterable

import django.db.models
from django.template.defaulttags import register

from emarket import config

__all__ = ["get_categories_batches",
           "get_prices_range",
           "spaces_to_dashes",
           "dashes_to_spaces",
           "underlines_to_spaces",
           "get_url_arg_from_bool",
           "get_element_by_index",
           "invert_sorting",
           "truncate",
           "round_"]


@register.filter
def get_categories_batches(categories: django.db.models.QuerySet):
    return [
        categories[listing: listing+config.MAIN_PAGE_CATEGORIES_BATCH_SIZE]
        for listing in range(0, len(categories), config.MAIN_PAGE_CATEGORIES_BATCH_SIZE)
    ]


@register.filter
def get_prices_range(max_item_price: float | int, min_item_price: float | int = 0) -> list:
    max_item_price, min_item_price = int(max_item_price), int(min_item_price)
    price_range = list(range(min_item_price, max_item_price, (1000 if max_item_price > 1500 else 300)))

    if price_range:
        if price_range[-1] < max_item_price:
            price_range.append(max_item_price)

    else:
        price_range.append(max_item_price)

    return price_range


@register.filter
def spaces_to_dashes(string: str) -> str:
    return string.replace(" ", "-") if string else string


@register.filter
def dashes_to_spaces(string: str) -> str:
    return string.replace("-", " ") if string else string


@register.filter
def underlines_to_spaces(string: str) -> str:
    return string.replace("_", " ")


@register.filter
def get_url_arg_from_bool(value: bool, name: str) -> str:
    return name if value else ""


@register.filter
def invert_sorting(sorting: str) -> str:
    try:
        return str(int(not bool(int(sorting))))
    except:
        return sorting


@register.filter
def round_(number: float, round_factor: int):
    try:
        return round(number=float(number), ndigits=int(round_factor))
    except:
        return number


@register.filter
def truncate(string: str, bound: int):
    return str(string)[:int(bound)]


@register.filter
def get_element_by_index(sequence: Iterable, idx: int) -> object:
    return sequence[int(idx)]
