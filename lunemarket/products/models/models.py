from typing import Union
from django.db import models
from products import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .models_utils import get_image_path


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Category name",
                             max_length=40,
                             unique=True,
                             validators=[validators.category_title_validator],
                             null=False)
    parent = models.ForeignKey(to="self",
                               to_field="title",
                               verbose_name="Parent category",
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_image_path,
                              null=False)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        _delete_photo(model=self)
        super().delete(using=using, keep_parents=keep_parents)

    def clean(self):
        if not self.parent and not self.title.isalpha():
            raise ValidationError("title of category without parent may contain only lowercase words and spaces")

    class Meta:
        db_table = "Categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Cards(models.Model):
    title = models.CharField("Name of product",
                             max_length=100,
                             unique=True,
                             validators=[validators.card_title_validator],
                             null=False,
                             primary_key=True)
    category = models.ForeignKey(to=Categories,
                                 to_field="title",
                                 verbose_name="Category name",
                                 null=False,
                                 on_delete=models.DO_NOTHING)
    photo = models.ImageField(upload_to=get_image_path,
                              null=False,
                              verbose_name="Card title photo")
    price = models.FloatField(verbose_name="Price of product",
                              validators=[MinValueValidator(0), MaxValueValidator(5000)])

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        _delete_photo(model=self)
        super().delete(using=using, keep_parents=keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.title.replace(" ", "-")
        return super(Cards, self).save(force_insert=force_insert,
                                       force_update=force_update,
                                       using=using,
                                       update_fields=update_fields)

    class Meta:
        db_table = "Cards"
        verbose_name = "Card"
        verbose_name_plural = "Cards"


def _delete_photo(model: Union[Categories, Cards]):
    model.photo.delete(save=True)
