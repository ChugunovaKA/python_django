from django import forms

from shopapp.models import Product

class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.FileInput(attrs={"multiple": True}),  # изменено с ClearableFileInput на FileInput
        required=False,
    )

    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
