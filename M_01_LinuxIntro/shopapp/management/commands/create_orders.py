from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product

class Command(BaseCommand):
    help = 'Create sample orders and link them to existing products'

    def handle(self, *args, **kwargs):
        # Получим пользователя (например, первого суперпользователя)
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR('No superuser found to assign orders'))
            return

        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR('No products found to add to orders'))
            return

        orders_data = [
            {
                'address': '123 Main St',
                'phone': '+1234567890',
                'products': products[:2],  # первые два продукта
            },
            {
                'address': '456 Side Ave',
                'phone': '+0987654321',
                'products': products[1:],  # все кроме первого
            },
        ]

        for data in orders_data:
            order, created = Order.objects.get_or_create(
                address=data['address'],
                phone=data['phone'],
                user=user,
            )
            order.products.set(data['products'])
            order.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created order #{order.id}"))
            else:
                self.stdout.write(f"Order #{order.id} already exists")