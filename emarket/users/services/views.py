from django.shortcuts import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from allauth.account.utils import send_email_confirmation

from . import urls
from ..utils import profile_errors
from ..utils.profile_errors import email_errors, username_errors


def confirm_user_email(request: HttpRequest, email: str) -> HttpResponseRedirect:
    try:
        send_email_confirmation(request=request, user=request.user, email=email)
    except Exception as exception:
        return HttpResponseRedirect(
            urls.get_url_with_args(
                url=request.path,
                error=(email_errors.ExistsEmailError.code
                       if exception == IntegrityError else
                       email_errors.UnexpectedEmailError.code)
        ))

    return HttpResponseRedirect( # pragma: no cover
        reverse("account_email_verification_sent")
    )

def get_username_error_code(validation_error: ValidationError, field_name: str) -> str:
    validation_error_message = validation_error.error_dict[field_name][0].message

    for error in profile_errors.USERNAME_ERRORS:
        if validation_error_message == error.message:
            return error.code

    return username_errors.UnexpectedUsernameError.code
