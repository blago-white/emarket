from .models.models import Cards, Categories
from django.forms import ModelForm, TextInput, ModelChoiceField, FileInput, NumberInput, URLField, IntegerField


class DeleteProductForm(ModelForm):
    category = ModelChoiceField(queryset=Categories.objects.all(),
                                empty_label=None,
                                required=True)

    class Meta:
        model = Cards
        fields = ["title", "category", "photo", "price"]
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
