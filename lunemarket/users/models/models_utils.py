from django.db import models


def get_image_path(self: models.Model, filename: str) -> str:
    return f"avatars/{self.user.id}.{filename.split('.')[-1]}"
