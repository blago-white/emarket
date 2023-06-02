from django.template.defaulttags import register


@register.filter
def get_media_path(path) -> str:
    return "../media/" + path
