from django.contrib import admin
from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Order.products.through  # для связи many-to-many


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'is_active')
    inlines = [OrderInline]  # показывать связанные заказы на странице продукта
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Цена', {'fields': ('price', 'quantity')}),
        ('Дополнительные опции', {'fields': ('is_active',), 'classes': ('collapse',)}),
    )
    search_fields = ('name', 'price')

    actions = ['make_inactive']

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} продуктов были архивированы.")

    make_inactive.short_description = "Архивировать выбранные продукты"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'phone', 'created_at')
    search_fields = ('address', 'phone')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

# Register your models here.
