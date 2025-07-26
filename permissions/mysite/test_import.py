import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")  # Убедитесь, что путь правильный
django.setup()

try:
    from shopapp.views import ShopIndexView
    print("Импорт ShopIndexView успешен")
except ImportError as e:
    print("Ошибка импорта ShopIndexView:")
    print(e)
except Exception as ex:
    print("Другая ошибка:")
    print(ex)