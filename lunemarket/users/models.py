from typing import Union
from django.db import models
from products import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Notifications(models.Model):
    NOTIFICATIONS_THEMES = [("inf", "info"), ("pur", "purchase")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Recipient of the notification", null=False)
    time = models.DateTimeField(verbose_name="Time of receipt", auto_now=True, null=False)
    theme = models.CharField(verbose_name="Theme of notification",
                             choices=NOTIFICATIONS_THEMES,
                             default=NOTIFICATIONS_THEMES[0])
    text = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.time}"

    class Meta:
        db_table = "Notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
