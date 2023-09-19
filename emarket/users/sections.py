from abc import ABCMeta, abstractmethod


class BaseAccountSection(metaclass=ABCMeta):
    def __repr__(self):
        return self.section_name

    def __str__(self):
        return self.section_name

    @property
    @abstractmethod
    def section_name(self):
        pass


class InfoAccountSection(BaseAccountSection):
    section_name = "info"


class ProductsAccountSection(BaseAccountSection):
    section_name = "products"


class BasketAccountSection(BaseAccountSection):
    section_name = "basket"


class NotificationsAccountSection(BaseAccountSection):
    section_name = "notifications"
