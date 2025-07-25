from django.urls import path

from .views import (
    ShopIndexView,
    ProductsListView,
    ProductCreateView,
    # ProductDeleteView временно убран
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    # path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),  # временно закомментировано
]