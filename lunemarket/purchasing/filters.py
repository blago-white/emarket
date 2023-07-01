from django.template.defaulttags import register

__all__ = ["get_media_path"]


@register.filter
def get_media_path(path) -> str:
    return "../media/" + path
