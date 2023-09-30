from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from .utils import get_image_path
from emarket import config

__all__ = ["Notifications", "UserProfile", "DistributionDeliveredMessage"]


@receiver(email_confirmed)
def _update_user_email(sender, request, email_address, **kwargs):
    email_address.set_as_primary()
    EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()


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
    avatar = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def clean(self):
        avatar: JpegImageFile = self.avatar

        try:
            photo_width, photo_height = avatar.image.size
        except:
            return self.avatar

        self._validate_photo_resolution(photo_width=photo_width, photo_height=photo_height)

        return self.avatar

    @staticmethod
    def _validate_photo_resolution(photo_width: int, photo_height: int) -> None:
        if photo_width < config.MINIMUM_PHOTO_RESOLUTION_WIDTH or photo_height < config.MINIMUM_PHOTO_RESOLUTION_HEIGHT:
            raise ValidationError(
                "Photo dimensions are too small (minimum: "
                f"width - {config.MINIMUM_PHOTO_RESOLUTION_WIDTH} "
                f"height - {config.MINIMUM_PHOTO_RESOLUTION_HEIGHT})"
            )

        elif photo_width > config.MAXIMUM_PHOTO_RESOLUTION_WIDTH or photo_height > config.MAXIMUM_PHOTO_RESOLUTION_HEIGHT:
            raise ValidationError("Photo dimensions are too large (maximum: "
                                  f"width - {config.MAXIMUM_PHOTO_RESOLUTION_WIDTH} "
                                  f"height - {config.MAXIMUM_PHOTO_RESOLUTION_HEIGHT})")

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
