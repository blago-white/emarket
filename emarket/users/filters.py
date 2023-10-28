import textwrap

from django.template.defaulttags import register
from django.http.request import HttpRequest

from .models.models import Notifications, DistributionDeliveredMessage

__all__ = ["enumerate_",
           "wrap",
           "get_title_theme",
           "show_notication_for_user",
           "get_user_ip_from_request"]


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


@register.filter
def show_notication_for_user(request: HttpRequest) -> bool:
    try:
        return not DistributionDeliveredMessage.objects.filter(
            ip=get_user_ip_from_request(request=request)
        ).exists() and (
                request.path.startswith("/accounts") or request.path == "/"
        )
    except:
        return False


@register.filter
def get_user_ip_from_request(request: HttpRequest) -> str | None:
    try:
        return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
    except:
        return None
