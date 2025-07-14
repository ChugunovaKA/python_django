from django.core.management.base import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    help = 'Create sample products using get_or_create'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Product 1',
                'description': 'Description for product 1',
                'price': 10.99,
                'quantity': 100,
                'is_active': True,
            },
            {
                'name': 'Product 2',
                'description': 'Description for product 2',
                'price': 20.50,
                'quantity': 50,
                'is_active': True,
            },
            # Добавь другие продукты по необходимости
        ]

        for prod in products:
            product_obj, created = Product.objects.get_or_create(
                name=prod['name'],
                defaults={
                    'description': prod['description'],
                    'price': prod['price'],
                    'quantity': prod['quantity'],
                    'is_active': prod['is_active'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product_obj.name}"))
            else:
                self.stdout.write(f"Product already exists: {product_obj.name}")