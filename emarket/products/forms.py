from PIL.JpegImagePlugin import JpegImageFile
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, ModelChoiceField, FileInput, NumberInput, ChoiceField

from .models.models import Category, Phone

__all__ = ["AddProductForm", "EditProductForm"]


class AddProductForm(ModelForm):
    category = ModelChoiceField(
        queryset=Category.objects.exclude(title__in=Phone.objects.select_related("category").values("title")),
        empty_label=None,
        required=True
    )
    color = ChoiceField(choices=Phone.BASE_COLORS,
                        required=True,
                        initial="red")
    storage = ChoiceField(choices=Phone.STORTAGE_SIZES,
                          required=True,
                          initial="128")

    class Meta:
        model = Phone
        fields = ["title", "category", "photo", "price", "color", "storage", "products_count"]
        widgets = {
            "title": TextInput(attrs={
                "required": True
            }),
            "photo": FileInput(attrs={
                "id": "upload-photo",
                "accept": "image/*",
                "style": "display: none",
            }),
            "price": NumberInput(attrs={"required": True, "min": 1, "max": 5000, "value": 100}),
        }

    def clean_photo(self):
        photo_field: JpegImageFile = self.cleaned_data.get('photo', None)

        if not photo_field:
            raise ValidationError("Photo does not exist!")

        try:
            photo_width, photo_height = photo_field.image.size
        except:
            return photo_field

        if photo_width < 300 or photo_height < 500:
            raise ValidationError("Photo dimensions are too small (minimum: width - 300 height - 500)")

        elif photo_width > 4500 or photo_height > 5000:
            raise ValidationError("Photo dimensions are too large (maximum: width - 4500 height - 5000)")

        return photo_field


class EditProductForm(AddProductForm):
    category = None

    class Meta:
        model = Phone
        fields = ["title", "photo", "price", "color", "storage", "products_count"]
        widgets = {
            "title": TextInput(attrs={
                "required": True
            }),
            "photo": FileInput(attrs={
                "id": "upload-photo",
                "accept": "image/*",
                "style": "display: none",
            }),
            "price": NumberInput(attrs={"required": True, "min": 1, "max": 5000, "value": 100}),
        }
