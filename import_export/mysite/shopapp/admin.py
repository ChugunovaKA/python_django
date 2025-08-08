import csv
from io import TextIOWrapper

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Product, Order, ProductImage

User = get_user_model()


class ImportOrdersForm(forms.Form):
    csv_file = forms.FileField(label="Выберите CSV файл для импорта заказов")


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request, queryset):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request, queryset):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = ("pk", "name", "description_short", "price", "discount", "archived")
    list_display_links = ("pk", "name")
    ordering = ("-name", "pk")
    search_fields = ("name", "description")
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Images", {
            "fields": ("preview",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for soft delete",
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class ProductInlineForOrder(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInlineForOrder,
    ]
    list_display = ("delivery_address", "promocode", "created_at", "user_verbose")

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    # Добавляем кастомный URL для импорта
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='shopapp_order_import_csv'
            ),
        ]
        return custom_urls + urls

    # Обработчик страницы импорта CSV
    def import_csv(self, request):
        if request.method == "POST":
            form = ImportOrdersForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)
                created_count = 0
                errors = []

                for row_number, row in enumerate(reader, start=2):
                    user_id = row.get('user_id')
                    if not user_id:
                        errors.append(f"Строка {row_number}: отсутствует user_id")
                        continue

                    try:
                        user = User.objects.get(pk=int(user_id))
                    except (User.DoesNotExist, ValueError):
                        errors.append(f"Строка {row_number}: пользователь с id={user_id} не найден или id некорректен")
                        continue

                    order = Order.objects.create(
                        user=user,
                        delivery_address=row.get('delivery_address', ''),
                        promocode=row.get('promocode', ''),
                    )

                    product_ids = row.get('product_ids', '')
                    if product_ids:
                        product_id_strs = [pid.strip() for pid in product_ids.split(',')]
                        valid_ids = []
                        invalid_ids = []

                        for pid_str in product_id_strs:
                            if pid_str.isdigit():
                                valid_ids.append(int(pid_str))
                            else:
                                invalid_ids.append(pid_str)

                        if invalid_ids:
                            errors.append(f"Строка {row_number}: некорректные ID товаров: {', '.join(invalid_ids)}")

                        products = Product.objects.filter(pk__in=valid_ids)
                        found_ids = set(p.pk for p in products)
                        missing_ids = set(valid_ids) - found_ids
                        if missing_ids:
                            errors.append(f"Строка {row_number}: товары с id {', '.join(map(str, missing_ids))} не найдены")

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

    # Добавляем в контекст changelist URL на импорт
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['import_url'] = reverse('admin:shopapp_order_import_csv')
        return super().changelist_view(request, extra_context=extra_context)