from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


__all__ = ["send_notification"]


@shared_task
def send_notification(message: str, recipient_mail: str, subject: str = "info") -> None:
    send_mail(subject=subject,
              recipient_list=[recipient_mail],
              from_email=settings.DEFAULT_FROM_EMAIL,
              message=str(),
              html_message=message)
