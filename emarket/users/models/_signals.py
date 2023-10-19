import os

from allauth.account.models import EmailAddress
from django.conf import settings

from .utils import get_image_path


def on_update_user_email(sender, request, email_address, **kwargs):
    email_address.set_as_primary()
    EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()


def on_profile_photo_update(instance, **_):
    future_avatar_path = "".join((
            str(settings.MEDIA_ROOT) + "/" + get_image_path(self=instance)
    ))

    if os.path.isfile(path=future_avatar_path):
        os.remove(future_avatar_path)
