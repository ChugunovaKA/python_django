from django.urls import path

from .views import shop_index, groups_list, ProductListView, orders_list

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),  # изменили на CBV
    path("orders/", orders_list, name="orders_list"),
]