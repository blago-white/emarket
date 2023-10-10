from .base import BaseEmailError


class ExistsEmailError(BaseEmailError):
    code = "exist-email"
    message = "A user with that email already exists."


class UnexpectedEmailError(BaseEmailError):
    code = "unexpected-error-email"
    message = "Unexpected error with email, try other."

