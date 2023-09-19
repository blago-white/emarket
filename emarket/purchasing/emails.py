from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from products.models.models import Phone
from . import PURCHASE_MESSAGE_FOR_OWNER_HTML_TEMPLATE, PURCHASE_MESSAGE_FOR_PURCHASER_HTML_TEMPLATE

__all__ = ["EmailPurchaseNotification", "send_notification"]


class _BaseEmailNotification:
    recipient_mail: str
    recipient_name: str
    recipient_id: int

    def __init__(self, recipient: User):
        self.recipient_mail = recipient.email
        self.recipient_name = recipient.username
        self.recipient_id = recipient.id


class EmailPurchaseNotification(_BaseEmailNotification):
    def __init__(self, purchaser: User):
        super(EmailPurchaseNotification, self).__init__(recipient=purchaser)

    def send_notification(self, product: Phone) -> None:
        self._send_purchase_message(purchase_message_template=PURCHASE_MESSAGE_FOR_OWNER_HTML_TEMPLATE,
                                    product=product,
                                    recipient_mail=product.author.email,
                                    user_id=self.recipient_id)
        self._send_purchase_message(purchase_message_template=PURCHASE_MESSAGE_FOR_PURCHASER_HTML_TEMPLATE,
                                    product=product,
                                    recipient_mail=self.recipient_mail,
                                    user_id=product.author.id)

    def _send_purchase_message(self, purchase_message_template: str,
                               product: Phone,
                               recipient_mail: str,
                               user_id: int) -> None:
        message = purchase_message_template.format(username=self.recipient_name,
                                                   productname=product.readable_title(),
                                                   usermail=self.recipient_mail,
                                                   price=product.price,
                                                   userid=user_id,
                                                   productid=product.id)

        send_notification(message=message, recipient_mail=recipient_mail, subject="purchase")


def send_notification(message: str, recipient_mail: str, subject: str = "info") -> None:
    send_mail(subject=subject,
              recipient_list=[recipient_mail],
              from_email=settings.DEFAULT_FROM_EMAIL,
              message=str(),
              html_message=message)
