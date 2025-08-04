from django import forms
from django.forms import FileInput

from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=FileInput(),  # без multiple=True, чтобы избежать ошибки
    )