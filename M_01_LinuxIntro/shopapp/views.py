from django.shortcuts import render
from datetime import date
from shopapp.models import Product, Order

def index(request):
    products = [
        {'name': 'Телефон', 'price': 19999.99},
        {'name': 'Ноутбук', 'price': 55999.49},
        {'name': 'Наушники', 'price': 2999.95},
    ]
    context = {
        'products': products,
        'today': date.today(),
        'greeting': 'Добро пожаловать в наш магазин!',
        'description': 'Лучшие товары по лучшим ценам для вас и вашей семьи.',
    }
    return render(request, 'shopapp/index.html', context)

def products_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'shopapp/products_list.html', context)

def orders_list(request):
    orders = Order.objects.select_related('user').prefetch_related('products').all()
    context = {
        'orders': orders,
    }
    return render(request, 'shopapp/orders_list.html', context)