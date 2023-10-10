from abc import ABCMeta, abstractmethod

from emarket.config import AVAILABLE_FOR_CHANGE_PROFILE_FIELDS


class BaseUserProfieDataError(metaclass=ABCMeta): # pragma: no cover
    code: str
    field: str
    message: str

    def __str__(self):
        return self.code

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def message(self) -> str:
        pass


class BaseUsernameError(BaseUserProfieDataError, metaclass=ABCMeta):
    field = AVAILABLE_FOR_CHANGE_PROFILE_FIELDS[0]


class BaseEmailError(BaseUserProfieDataError, metaclass=ABCMeta):
    field = AVAILABLE_FOR_CHANGE_PROFILE_FIELDS[1]
