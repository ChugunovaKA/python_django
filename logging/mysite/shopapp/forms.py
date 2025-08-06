from django import forms
from shopapp.models import Product

class ProductForm(forms.ModelForm):
    # Поле для множественной загрузки изображений
    images = forms.ImageField(
        widget=forms.FileInput(attrs={"multiple": True}),
        required=False  # если поле необязательно
    )

    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview")