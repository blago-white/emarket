from django.contrib.auth.models import User

from .base import BaseUsernameError


class UncorrectUsernameError(BaseUsernameError):
    code = "uncorrect-username"
    message = User.username_validator.message


class ExistsUsernameError(BaseUsernameError):
    code = "exist-username"
    message = "A user with that username already exists."


class UnexpectedUsernameError(BaseUsernameError):
    code = "unexpected-error-username"
    message = "Unexpected error with username, try other."

