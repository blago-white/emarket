from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from .utils import get_image_path


__all__ = ["Notifications", "UserProfile"]


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True, unique=True)
    avatar = models.ImageField(upload_to=get_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def clean(self):
        avatar: JpegImageFile = self.avatar

        try:
            photo_width, photo_height = avatar.image.size
        except:
            return self.avatar

        if photo_width < 300 or photo_height < 300:
            raise ValidationError("Photo dimensions are too small (minimum: width - 300 height - 500)")

        elif photo_width > 4500 or photo_height > 5000:
            raise ValidationError("Photo dimensions are too large (maximum: width - 4500 height - 5000)")

        return self.avatar

    class Meta:
        db_table = "users_profiles"
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"
