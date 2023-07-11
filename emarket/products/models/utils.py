import hashlib
import random

from django.db import models
from django.db.models import F

from .. import filters

__all__ = ["get_image_path", "decrease_phones_count", "delete_photo", "increment_product_views"]


def get_image_path(self: models.Model, filename: str) -> str:
    return _form_load_path_to_image(target_dir=_get_target_directory(model=self),
                                    img_hash=_get_image_name(filename=filename),
                                    img_extension=_get_file_extension(filename=filename),
                                    object_title=self.title)


def decrease_phones_count(phone: models.Model) -> None:
    if int(phone.products_count) <= 0:
        raise ValueError

    phone.products_count = F("products_count") - 1
    phone.save()


def increment_product_views(phone: models.Model) -> None:
    phone.views = F("views") + 1
    phone.save()


def delete_photo(model: models.Model):
    model.photo.delete(save=True)


def convert_category_filters_to_product_filters(query_filters: dict) -> None:
    for query_filter_column, query_filter_value in tuple(zip(query_filters.keys(), query_filters.values())):
        if not ("phone__" in query_filter_column):
            continue

        query_filters[query_filter_column.replace("phone__", "")] = query_filters[query_filter_column]
        del query_filters[query_filter_column]


def _form_load_path_to_image(**path_parts: dict) -> str:
    try:
        target_dir = path_parts['target_dir']
        object_title = filters.spaces_to_dashes(path_parts['object_title'])
        image_name = ".".join((path_parts['img_hash'], path_parts['img_extension']))

        return '/'.join((target_dir, object_title, image_name))

    except KeyError:
        raise KeyError(f"Not all arguments for making a path have been received, received: {path_parts.keys()}")


def _get_image_name(filename: str) -> str:
    filename = "".join(random.choice(list(filename)))
    return hashlib.sha256(filename.encode("utf-8")).hexdigest()


def _get_target_directory(model: models.Model) -> str:
    return model.__class__.__name__.lower()


def _get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]
