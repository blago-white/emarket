from allauth.socialaccount.models import SocialAccount
from django.conf import settings

from users.models.models import UserProfile


def get_user_avatar_url(user_id: int) -> str | None:
    try:
        profile_avatar_name = UserProfile.objects.get(user__id=user_id).avatar.name
    except UserProfile.DoesNotExist:
        return SocialAccount.objects.get(user__id=user_id).get_avatar_url()
    except:
        return

    return str(settings.MEDIA_URL) + profile_avatar_name if profile_avatar_name else None


def get_username_by_mail(mail_adress: str) -> str:
    return "".join(letter for letter in mail_adress.split("@")[0] if letter.isalpha())
