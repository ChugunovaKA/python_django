from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, data):
        # Ожидаем, что data — это список файлов
        if not data:
            return None
        elif isinstance(data, list):
            return data
        else:
            return [data]

    def validate(self, data):
        # Если список файлов с несколькими элементами
        if isinstance(data, list):
            for file in data:
                super().validate(file)
        else:
            super().validate(data)

    def clean(self, data, initial=None):
        if not data:
            return None
        if not isinstance(data, list):
            data = [data]
        cleaned_data = []
        errors = []
        for file in data:
            try:
                cleaned_file = super().clean(file, initial)
                cleaned_data.append(cleaned_file)
            except forms.ValidationError as e:
                errors.append(e)
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class ProductForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview",)