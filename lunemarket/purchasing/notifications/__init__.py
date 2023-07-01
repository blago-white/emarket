from users.models.models import Notifications


def try_save_notification(notification: Notifications) -> None:
    notification.full_clean()
    notification.save()
