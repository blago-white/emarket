from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware.csrf import get_token

def get_reset_password_request(user: User) -> HttpRequest:
    request = HttpRequest()

    request.method, request.user = 'POST', user
    request.META['HTTP_HOST'] = settings.HOST_NAME

    request.POST = {
        'email': user.email,
        'csrfmiddlewaretoken': get_token(request)
    }

    return request
