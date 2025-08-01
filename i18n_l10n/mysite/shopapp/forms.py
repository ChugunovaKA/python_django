from django import forms
from shopapp.models import Product
# Импортируйте свою модель для изображений, если есть
# from shopapp.models import ProductImage


class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(),
        required=False  # чтобы не было ошибки, если не загрузить файлы
    )

    class Meta:
        model = Product
        fields = ("name", "price", "description", "discount", "preview")

    def save(self, commit=True):
        # Сначала сохраняем основную модель Product
        instance = super().save(commit=commit)

        # Обрабатываем загруженные изображения (если они есть)
        images = self.files.getlist('images')
        for image in images:
            # Пример сохранения связанных изображений
            # Предположим, есть модель ProductImage с ForeignKey к Product
            # ProductImage.objects.create(product=instance, image=image)
            pass  # Здесь добавьте реальную логику сохранения изображений

        return instance