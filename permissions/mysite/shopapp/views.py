from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy

from .models import Product

class ShopIndexView(TemplateView):
    template_name = "shopapp/index.html"

class ProductsListView(ListView):
    model = Product
    template_name = "shopapp/products_list.html"
    context_object_name = "products"

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ("name", "price", "description", "discount")
    template_name = "shopapp/product_create.html"
    success_url = reverse_lazy("shopapp:products_list")
    permission_required = "shopapp.add_product"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)