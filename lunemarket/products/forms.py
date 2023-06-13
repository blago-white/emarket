from .models.models import Category, Phone
from django.forms import ModelForm, TextInput, ModelChoiceField, FileInput, NumberInput, URLField, IntegerField, \
    ChoiceField


class AddProductForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(),
                                empty_label=None,
                                required=True)
    color = ChoiceField(choices=Phone.BASE_COLORS,
                        required=True,
                        initial="red")
    stortage = ChoiceField(choices=Phone.STORTAGE_SIZES,
                           required=True,
                           initial="128")

    class Meta:
        model = Phone
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


class AddCategoryForm(ModelForm):
    parent = ModelChoiceField(queryset=Category.objects.all(),
                              empty_label="",
                              required=False)

    class Meta:
        model = Category
        fields = ["title", "parent", "photo"]

        widgets = {
            "title": TextInput(attrs={
                "required": True
            }),
            "photo": FileInput(attrs={
                "id": "upload-photo",
                "accept": "image/*",
                "style": "display: none",
                "required": True
            }),
        }
