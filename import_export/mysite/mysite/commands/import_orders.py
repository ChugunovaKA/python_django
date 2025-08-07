from django.core.management.base import BaseCommand, CommandError
from shopapp.models import Order, Product  # подкорректируйте по вашей модели
import csv  # или json, xml в зависимости от формата


class Command(BaseCommand):
    help = "Импорт заказов из файла CSV"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Путь к файлу для импорта заказов.")

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Пример обработки строки, подкорректируйте под ваши поля модели Order
                    order = Order.objects.create(
                        user_id=row['user_id'],
                        status=row['status'],
                        # заполните нужные поля
                    )
                    # Если есть связь с продуктами – добавьте дополнительные действия

                    self.stdout.write(self.style.SUCCESS(f"Заказ {order.pk} импортирован."))

        except FileNotFoundError:
            raise CommandError(f"Файл {file_path} не найден.")
        except Exception as e:
            raise CommandError(f"Ошибка при импорте: {e}")