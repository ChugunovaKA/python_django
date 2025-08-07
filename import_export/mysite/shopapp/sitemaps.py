from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        # Если в модели Product есть поле с датой обновления, например updated_at,
        # замените на ваше имя поля.
        return getattr(obj, 'updated_at', None)

    def location(self, obj):
        return obj.get_absolute_url()