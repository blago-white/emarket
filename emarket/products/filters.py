from typing import Iterable

import django.db.models
from django.conf import settings
from django.template.defaulttags import register


__all__ = ["get_categories_batches",
           "get_prices_range",
           "spaces_to_dashes",
           "dashes_to_spaces",
           "underlines_to_spaces",
           "get_url_arg_from_bool",
           "get_url_arg_from_ordering_field",
           "get_ordering_field_from_url_arg",
           "get_element_by_index",
           "compile_url_args_for_pagination",
           "invert_sorting",
           "truncate",
           "round_"]


@register.filter
def get_categories_batches(categories: django.db.models.QuerySet):
    return [
        categories[listing: listing+settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE]
        for listing in range(0, len(categories), settings.MAIN_PAGE_CATEGORIES_BATCH_SIZE)
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


def compile_url_args_for_pagination(**url_kwargs) -> str:
    url_args = str()

    for arg_name in url_kwargs:
        if type(url_kwargs[arg_name]) in (list, set, frozenset, tuple):
            for value in url_kwargs[arg_name]:
                url_args += f"&{arg_name.replace('_', '')}={value}" if value is not None else ""
        else:
            url_args += f"&{arg_name.replace('_', '')}={url_kwargs[arg_name]}" if url_kwargs[arg_name] is not None else ""

    return url_args


def get_ordering_field_from_url_arg(url_arg: str, field: str) -> str:
    try:
        return field if not int(url_arg) else "-" + field
    except:
        return field


def get_url_arg_from_ordering_field(field: str) -> int:
    return int(field.startswith("-"))
