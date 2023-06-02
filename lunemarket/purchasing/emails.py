from django.core.mail import send_mail


class Email:
    admin_mail = "bogdanloginov31@gmail.com"


class EmailPurchase(Email):
    _user_purchase_message_form = "Hi, {name}, you ordered the {productname} for the price of {price}"

    def __init__(self, username: str, user_mail: str, fail_silently: str = True):
        self._user_mail = user_mail
        self._username = username
        self._fail_silently = fail_silently

    def send(self, product_title: str, price: int) -> None:
        message = self._fill_purchase_message_form(product_title=product_title, price=price)
        self._send_to_admin()
        self._send_to_user()

        send_mail(subject="purchase",
                  message=message,
                  from_email=self._user_mail,
                  fail_silently=self._fail_silently,
                  recipient_list=[super().admin_mail])

    def _fill_purchase_message_form(self, product_title: str, price: int) -> str:
        return self._user_purchase_message_form.format(name=self._username,
                                                       productname=product_title,
                                                       price=price)
