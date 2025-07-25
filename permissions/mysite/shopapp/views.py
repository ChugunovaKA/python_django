from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Product

class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ("name", "price", "description", "discount")
    permission_required = "shopapp.add_product"  # доступ к созданию продукта имеет пользователь с этим правом
    success_url = reverse_lazy("shopapp:products_list")

    # (опционально) если хотите задать страницу логина явно, если пользователь не залогинен:
    # login_url = reverse_lazy("accounts:login")

    # (опционально) чтобы отдавать 403 вместо редиректа:
    # raise_exception = True
