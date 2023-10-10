from PIL.JpegImagePlugin import JpegImageFile
from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save

from emarket import config

from . import utils
from . import _signals

__all__ = ["Notifications", "UserProfile", "DistributionDeliveredMessage"]


class Notifications(models.Model):
    NOTIFICATIONS_THEMES = [("inf", "info"), ("pur", "purchase")]

    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Initiator of the notification",
                               null=True,
                               blank=True,
                               related_name="senders")
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name="Recipient of the notification",
                                  null=False,
                                  related_name="recipients")
    time = models.DateTimeField(verbose_name="Time of receipt", auto_now=True, null=False)
    theme = models.CharField(verbose_name="Theme of notification",
                             choices=NOTIFICATIONS_THEMES,
                             default=NOTIFICATIONS_THEMES[0])
    text = models.CharField(max_length=500, null=False)

    def __str__(self):
        return f"{self.recipient.username} - {self.time}"

    def clean(self):
        if self.sender == self.recipient:
            raise ValidationError("The sender and the recipient must be different users")
        if not self.sender and self.theme != self.NOTIFICATIONS_THEMES[0][0]:
            raise ValidationError("If you want to send a message without an initiator, specify the theme = inf")

    class Meta:
        db_table = "users_notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=False,
                                primary_key=True,
                                unique=True,
                                related_name="profile")
    avatar = models.ImageField(upload_to=utils.get_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def clean(self): # pragma: no cover
        avatar: models.ImageField = self.avatar

        try:
            photo_width, photo_height = avatar.image.size
        except Exception as e:
            raise e
        else:
            utils.validate_avatar_resolution(photo_width=photo_width, photo_height=photo_height)

        return self.avatar

    class Meta:
        db_table = "users_profiles"
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"


class DistributionDeliveredMessage(models.Model):
    ip = models.GenericIPAddressField(verbose_name="User IP address", protocol="IPv4", null=False, primary_key=True)
    date = models.DateField(verbose_name="Date the user viewed the notification", auto_now=True, auto_created=True)

    def __str__(self):
        return f"Message for {self.ip} delivered"

    class Meta:
        db_table = "distribution_delivered_messages"
        verbose_name = "Distribution message delivered"
        verbose_name_plural = "Delivered distribution messages"


def _connect_receivers():
    email_confirmed.connect(receiver=_signals.on_update_user_email)
    pre_save.connect(receiver=_signals.on_profile_photo_update, sender=UserProfile)


_connect_receivers()
