import hashlib
import random

from os import listdir
from os.path import isfile, join
from django.db import models
from products import validators


def _get_image_name(filename: str) -> str:
    filename = ''.join(random.choice(list(filename)))
    return hashlib.sha256(filename.encode('utf-8')).hexdigest()


def _get_target_directory(model_dictionary: dict) -> str:
    return 'cards' if 'category' in model_dictionary else 'categories'


def _get_file_extension(filename: str) -> str:
    return filename.split('.')[-1]


def _get_img_upload_path(self: models.Model, filename: str) -> str:
    target_dir, img_hash, img_extension = (_get_target_directory(model_dictionary=self.__dict__),
                                           _get_image_name(filename=filename),
                                           _get_file_extension(filename=filename))
    return f"{target_dir}/{self.title}/{img_hash}.{img_extension}"


class Categories(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField("Category name",
                             max_length=40,
                             unique=True,
                             validators=[validators.category_title_validator, validators.duplicate_spaces_validator],
                             null=False)

    parent = models.ForeignKey(to="self",
                               to_field="title",
                               verbose_name="Parent category",
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)

    preview = models.ImageField(upload_to=_get_img_upload_path,
                                null=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Cards(models.Model):
    title = models.CharField("Name of product",
                             max_length=100,
                             unique=True,
                             validators=[validators.card_title_validator, validators.duplicate_spaces_validator],
                             null=False)

    category = models.ForeignKey(to=Categories,
                                 to_field="title",
                                 verbose_name="Category name",
                                 null=False,
                                 on_delete=models.DO_NOTHING)

    photo = models.ImageField(upload_to=_get_img_upload_path,
                              null=False,
                              verbose_name="Card title photo")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "Cards"
        verbose_name = "Card"
        verbose_name_plural = "Cards"
