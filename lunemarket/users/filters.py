import django.db.models
from django.template.defaulttags import register
from django.conf import settings
from .models import Notifications
import textwrap


@register.filter
def enumerate_(obj: list | tuple | set) -> enumerate:
    return enumerate(obj)


@register.filter
def wrap(string: str, line_length: int = 18) -> list[str]:
    return textwrap.wrap(string, line_length)


@register.filter
def get_title_theme(name: str) -> str:
    for name_theme, title_theme in Notifications.NOTIFICATIONS_THEMES:
        if name_theme == name:
            return title_theme
