from typing import Union

import django.conf
from django.db import models
from products import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from .models_utils import get_image_path
from ..filters import spaces_to_dashes


class Category(models.Model):
    title = models.CharField("Category name",
                             max_length=40,
                             unique=True,
                             validators=[validators.child_category_title_validator],
                             null=False,
                             primary_key=True)

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = spaces_to_dashes(self.title)
        return super().save(force_insert=force_insert,
                            force_update=force_update,
                            using=using,
                            update_fields=update_fields)

    def clean(self):
        if not self.parent and not self.title.isalpha():
            raise ValidationError("title of category without parent may contain only lowercase words and spaces")

        if not self.parent:
            validators.parent_category_title_validator(value=self.title)

    class Meta:
        db_table = "Categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BaseProduct(models.Model):
    title = models.CharField("Name of product",
                             max_length=100,
                             validators=[validators.card_title_validator],
                             null=False)

    category = models.ForeignKey(to=Category,
                                 verbose_name="Category name",
                                 null=False,
                                 on_delete=models.CASCADE)

    photo = models.ImageField(upload_to=get_image_path,
                              null=False,
                              verbose_name="Product title photo")

    price = models.FloatField(verbose_name="Price of product",
                              validators=[MinValueValidator(0), MaxValueValidator(5000)])

    views = models.IntegerField(verbose_name="Number views per product",
                                null=True,
                                default=0)

    products_count = models.PositiveSmallIntegerField(verbose_name="Number of items of this product",
                                                      null=False,
                                                      default=1,
                                                      validators=[MinValueValidator(1), MaxValueValidator(10000)])

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Creator's account",
                               null=False)

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
        _delete_photo(model=self)

        try:
            category = Category.objects.get(title=self.title)
        except:
            pass
        else:
            products_with_current_category = BaseProduct.objects.filter(category=category)

            if products_with_current_category.count() == 1:
                products_with_current_category[0].category = category.parent
                category.delete()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = spaces_to_dashes(self.title)
        return super().save(force_insert=force_insert,
                            force_update=force_update,
                            using=using,
                            update_fields=update_fields)


class Phone(BaseProduct):
    BASE_COLORS = [("#FFEDDA", "white"),
                   ("#E4717A", "red"),
                   ("#FCE883", "yellow"),
                   ("#A8E4A0", "green"),
                   ("#AFDAFC", "blue"),
                   ("#CCCCFF", "purple"),
                   ("#222222", "black")]

    STORTAGE_SIZES = [(1, 64),
                      (2, 128),
                      (3, 256),
                      (4, 512),
                      (5, 1024)]

    COLOR_CODE_BY_NAME = {color_name: color_code for color_code, color_name in BASE_COLORS}

    color = models.CharField(verbose_name="Color of product",
                             choices=BASE_COLORS,
                             null=False,
                             blank=False)

    stortage = models.PositiveSmallIntegerField(verbose_name="Stortage size",
                                                choices=STORTAGE_SIZES,
                                                null=False,
                                                blank=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Phones"
        verbose_name = "Phone"
        verbose_name_plural = "Phones"


def _delete_photo(model: Union[Category]):
    model.photo.delete(save=True)
