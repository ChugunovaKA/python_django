import csv
from io import TextIOWrapper

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

from .models import Order, Product


class ImportOrdersForm(forms.Form):
    csv_file = forms.FileField(label="Выберите CSV файл для импорта заказов")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    # --- Новый код для импорта ---

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='shopapp_order_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = ImportOrdersForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)
                created_count = 0
                errors = []
                for row_number, row in enumerate(reader, start=2):
                    # Пример: ожидаем в CSV поля user_id, delivery_address, promocode, product_ids (через запятую)
                    user_id = row.get('user_id')
                    if not user_id:
                        errors.append(f"Строка {row_number}: отсутствует user_id")
                        continue

                    try:
                        user = self.model._meta.app_label == 'auth' and self.model._meta.model_name == 'user' and None or None
                        # Лучше импортировать User в начало файла и использовать:
                        # from django.contrib.auth.models import User
                        from django.contrib.auth import get_user_model
                        User = get_user_model()
                        user = User.objects.get(pk=int(user_id))
                    except Exception:
                        errors.append(f"Строка {row_number}: пользователь с id={user_id} не найден")
                        continue

                    order = Order.objects.create(
                        user=user,
                        delivery_address=row.get('delivery_address', ''),
                        promocode=row.get('promocode', ''),
                    )
                    product_ids = row.get('product_ids', '')
                    if product_ids:
                        ids_list = [int(pid.strip()) for pid in product_ids.split(',') if pid.strip().isdigit()]
                        products = Product.objects.filter(pk__in=ids_list)
                        order.products.set(products)

                    created_count += 1

                if errors:
                    for error in errors:
                        self.message_user(request, error, level=messages.ERROR)

                self.message_user(request, f"Успешно импортировано заказов: {created_count}", level=messages.SUCCESS)
                return HttpResponseRedirect("../")
        else:
            form = ImportOrdersForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
        )
        return render(request, "admin/csv_form.html", context)
