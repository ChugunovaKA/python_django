from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Product

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')  # поля редактирования
    template_name = 'shopapp/product_update.html'          # путь к шаблону
    success_url = reverse_lazy('shopapp:products_list')    # куда переходит после сохранения

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # Суперпользователь всегда может редактировать
        # Остальные — только если есть разрешение и автор продукта
        return user.is_superuser or (user.has_perm('shopapp.change_product') and product.created_by == user)