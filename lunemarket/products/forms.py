from django.forms import ModelForm, TextInput, ModelChoiceField, FileInput, NumberInput, ChoiceField

from .models.models import Category, Phones


__all__ = ["AddProductForm", "EditProductForm"]


class AddProductForm(ModelForm):
    category = ModelChoiceField(
        queryset=Category.objects.exclude(title__in=Phones.objects.select_related("category").values("title")),
        empty_label=None,
        required=True
    )
    color = ChoiceField(choices=Phones.BASE_COLORS,
                        required=True,
                        initial="red")
    stortage = ChoiceField(choices=Phones.STORTAGE_SIZES,
                           required=True,
                           initial="128")

    class Meta:
        model = Phones
        fields = ["title", "category", "photo", "price", "color", "stortage", "products_count"]
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


class EditProductForm(AddProductForm):
    category = None

    class Meta:
        model = Phones
        fields = ["title", "photo", "price", "color", "stortage", "products_count"]
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
