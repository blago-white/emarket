from django.template.defaulttags import register
from django.conf import settings

__all__ = ["get_media_path"]


@register.filter
def get_media_path(path) -> str:
    return "../uploads/" + path
