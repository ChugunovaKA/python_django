from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)  # CharField
    description = models.TextField()          # TextField
    price = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField
    quantity = models.PositiveSmallIntegerField()  # PositiveSmallIntegerField
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField
    is_active = models.BooleanField(default=True)  # BooleanField

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Order(models.Model):
    address = models.TextField()  # TextField
    phone = models.CharField(max_length=20)  # CharField
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь с User
    products = models.ManyToManyField(Product)  # связь с Product

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"