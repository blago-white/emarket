from allauth.socialaccount.models import SocialAccount
from django.conf import settings

from users.models.models import UserProfile


def get_user_avatar_url(user_id: int) -> str | None:
    try:
        profile_avatar_name = UserProfile.objects.get(user__id=user_id).avatar.name
        return str(settings.MEDIA_URL) + profile_avatar_name if profile_avatar_name else None
    except UserProfile.DoesNotExist:
        try:
            return SocialAccount.objects.get(user_id=user_id).get_avatar_url()
        except:
            pass
    except:
        pass


def get_username_by_mail(mail_adress: str) -> str:
    return "".join(letter for letter in mail_adress.split("@")[0] if letter.isalpha())
