from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy

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
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'discount']
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:products_list')


class ProductArchiveView(UpdateView):
    model = Product
    fields = []  # Пустое поле, пользователь ничего не редактирует
    template_name = 'shopapp/product_archive_confirm.html'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.archived = True
        return super().form_valid(form)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)