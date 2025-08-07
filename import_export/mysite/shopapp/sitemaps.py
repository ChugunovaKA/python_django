from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Возвращаем только неархивированные продукты, если применимо
        return Product.objects.filter(archived=False)

    def lastmod(self, obj):
        # Используем 'created_at', так как 'updated_at' отсутствует
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()