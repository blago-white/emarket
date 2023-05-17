from django.db import models
from . import validators


def get_img_upload_path(self, filename: str) -> str:
    return f"{self.title}/images/{filename}"


class Categories(models.Model):
    title = models.CharField("Category name",
                             max_length=40,
                             primary_key=True,
                             unique=True,
                             validators=[validators.category_name_validator],
                             null=False)

    preview = models.ImageField(upload_to=get_img_upload_path,
                                null=False,
                                default="media\\items_photos\\default\\default_preview.png")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "Categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
