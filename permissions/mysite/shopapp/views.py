from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy

from .models import Product

# Главная страница магазина (обязательный класс, чтобы устранить ошибку импорта ShopIndexView)
class ShopIndexView(TemplateView):
    template_name = "shopapp/index.html"


# Создание продукта с проверкой разрешения
class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ("name", "price", "description", "discount")
    permission_required = "shopapp.add_product"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Класс списка продуктов
class ProductsListView(ListView):
    model = Product
    template_name = "shopapp/products_list.html"
    context_object_name = "products"