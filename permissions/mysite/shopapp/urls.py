from django.urls import path
from .views import ProductUpdateView, ProductsListView, ProductCreateView

app_name = "shopapp"

urlpatterns = [
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
]