from django.urls import path

from .views import (
    shop_index,
    groups_list,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    product_archive,  # импортируем функцию архивации
    orders_list,
)

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("products/archive/<int:pk>/", product_archive, name="product_archive"),  # маршрут для архивации
    path("orders/", orders_list, name="orders_list"),
]
