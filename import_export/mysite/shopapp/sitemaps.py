from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # если у модели Product есть поле updated_at
        # иначе можно вернуть None или другое поле с датой изменения

    def location(self, obj):
        return obj.get_absolute_url()