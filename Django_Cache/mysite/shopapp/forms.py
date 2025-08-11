from django import forms
from shopapp.models import Product  # Импорт модели Product из shopapp.models


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview",)


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()