from django.shortcuts import render

# Create your views here.
from datetime import date

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