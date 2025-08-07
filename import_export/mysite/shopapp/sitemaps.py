from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Возвращаем только неархивированные товары
        return Product.objects.filter(archived=False)

    def lastmod(self, obj):
        # Возвращаем дату создания, так как updated_at отсутствует
        return obj.created_at

    def location(self, obj):
        # Возвращаем URL товара через get_absolute_url()
        # Можно заменить на reverse(), если требуется
        return obj.get_absolute_url()