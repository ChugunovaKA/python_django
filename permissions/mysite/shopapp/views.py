from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Product

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ("name", "price", "description", "discount")
    template_name = "shopapp/product_create.html"  # проверьте путь к шаблону
    success_url = reverse_lazy("shopapp:products_list")
    permission_required = "shopapp.add_product"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
