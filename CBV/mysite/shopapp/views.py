from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/products-list.html'  # используем уже существующий шаблон
    context_object_name = 'products'

    def get_queryset(self):
        # Возвращаем только неархивированные продукты
        return Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'  # создадим этот шаблон
    context_object_name = 'product'


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)
