from . import username_errors, email_errors, base


__all__  = ["USERNAME_ERRORS", "get_error_by_code"]


def _get_error_classes() -> tuple[base.BaseUserProfieDataError]:
    error_classes = list()

    for base_error_class in base.BaseUserProfieDataError.__subclasses__():
        error_classes.extend(base_error_class.__subclasses__())


    return tuple(error_classes)


_ERROR_CLASSES = _get_error_classes()

_ERROR_CLASS_FOR_ID = {
    error_class.code: error_class for error_class in _ERROR_CLASSES
}

USERNAME_ERRORS = (error_class for error_class in base.BaseUsernameError.__subclasses__())

def get_error_by_code(code: str) -> base.BaseUserProfieDataError | None:
    return _ERROR_CLASS_FOR_ID.get(code)
