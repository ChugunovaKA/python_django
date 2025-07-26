from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Product

class ProductsListView(ListView):
    model = Product
    template_name = 'shopapp/products_list.html'
    context_object_name = 'products'

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')
    template_name = 'shopapp/product_create.html'
    permission_required = 'shopapp.add_product'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = ('name', 'price', 'description', 'discount')
    template_name = 'shopapp/product_update.html'
    success_url = reverse_lazy('shopapp:products_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user.is_superuser or (user.has_perm('shopapp.change_product') and product.created_by == user)