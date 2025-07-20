from django import forms
from .models import Product, Order  # Импортируем обе модели

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'