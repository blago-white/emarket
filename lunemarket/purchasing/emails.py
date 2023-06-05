import django.conf
from django.core.mail import send_mail
from . import DEFAULT_PURCHASE_MESSAGE_FOR_ADMIN


class Email:
    admin_mail = "bogdanloginov31@gmail.com"


class EmailPurchase(Email):
    _admin_purchase_message_form = DEFAULT_PURCHASE_MESSAGE_FOR_ADMIN

    def __init__(self, username: str, user_mail: str, fail_silently: str = True):
        self._user_mail = user_mail
        self._username = username
        self._fail_silently = fail_silently

    def send(self, product_title: str, price: int) -> None:
        self._send_purchase_message_to_admin(product_title=product_title, price=price)

    def _send_purchase_message_to_admin(self, product_title: str, price: int) -> None:
        message = self._fill_purchase_message_form_to_admin(product_title=product_title, price=price)
        send_mail(subject="purchase",
                  from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
                  message=message,
                  fail_silently=self._fail_silently,
                  recipient_list=[self.admin_mail])

    def _fill_purchase_message_form_to_admin(self, product_title: str, price: int) -> str:
        return self._admin_purchase_message_form.format(username=self._username,
                                                        productname=product_title,
                                                        usermail=self._user_mail,
                                                        price=price)
