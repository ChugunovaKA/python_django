from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Product

class ProductsListView(ListView):
    model = Product
    template_name = 'shopapp/products_list.html'  # проверьте наличие этого шаблона
    context_object_name = 'products'

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')
    template_name = 'shopapp/product_create.html'  # проверьте наличие шаблона
    permission_required = 'shopapp.add_product'
    success_url = reverse_lazy('shopapp:products_list')