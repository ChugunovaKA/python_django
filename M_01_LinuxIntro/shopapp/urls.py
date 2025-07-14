from django.urls import path
from .views import index, products_list, orders_list  # импортируем все три view-функции

urlpatterns = [
    path('', index, name='index'),  # главная страница
    path('products/', products_list, name='products_list'),  # страница со списком продуктов
    path('orders/', orders_list, name='orders_list'),  # страница со списком заказов
]