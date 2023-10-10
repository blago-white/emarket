from django.db import models
from django.core.exceptions import ValidationError

from emarket import config


def validate_avatar_resolution(photo_width: int, photo_height: int) -> None:
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

    photo_aspect_ratio = max(photo_width, photo_height) / min(photo_width, photo_height)

    if photo_aspect_ratio > 3:
        raise ValidationError("The aspect ratio of the photo should not be more than 1/3 (or 3/1) "
                              f"now - 1/{photo_aspect_ratio}")


def get_image_path(self: models.Model, *_) -> str:
    return f"avatars/{self.user.id}.png"
