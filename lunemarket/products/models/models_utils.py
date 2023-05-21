import hashlib
import random

from django.db import models


def _get_image_name(filename: str) -> str:
    filename = ''.join(random.choice(list(filename)))
    return hashlib.sha256(filename.encode('utf-8')).hexdigest()


def _get_target_directory(model_dictionary: dict) -> str:
    return 'cards' if 'category' in model_dictionary else 'categories'


def _get_file_extension(filename: str) -> str:
    return filename.split('.')[-1]


def get_image_path(self: models.Model, filename: str) -> str:
    target_dir, img_hash, img_extension = (_get_target_directory(model_dictionary=self.__dict__),
                                           _get_image_name(filename=filename),
                                           _get_file_extension(filename=filename))
    return f"{target_dir}/{self.title.replace(' ', '_')}/{img_hash}.{img_extension}"
