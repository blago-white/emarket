import django.db.models
from django.template.defaulttags import register
from django.conf import settings
import textwrap


@register.filter
def enumerate_(obj: list | tuple | set) -> enumerate:
    return enumerate(obj)


@register.filter
def wrap(string: str) -> list[str]:
    return textwrap.wrap(string, 18)
