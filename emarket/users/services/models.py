from django.contrib.auth.models import User
from users.models.models import UserProfile

def try_update_user_profile_field(user: User | UserProfile, field: str, new_value: str) -> None:
    user.__dict__[field] = new_value
    user.full_clean()
    user.save()
