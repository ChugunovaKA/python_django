from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.syndication.views import Feed  # импорт для RSS
from django.contrib.auth.models import User
import csv
import tempfile

from .models import Product, Order, ProductImage
from .forms import ProductForm, ImportOrdersForm
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
        .all()
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


# Новый класс для RSS-ленты новейших товаров
class LatestProductsFeed(Feed):
    title = "Latest Products"
    link = "/products/latest/feed/"
    description = "Updates on the latest products added to the shop."

    def items(self):
        return Product.objects.order_by('-created_at')[:5]  # последние 5 продуктов

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


# Функция для импорта заказов из CSV-файла
def import_orders_from_file(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ожидаемые поля CSV: user_id, delivery_address, product_ids, promocode
            try:
                user = User.objects.get(pk=int(row['user_id']))
            except User.DoesNotExist:
                continue  # если пользователь не найден, пропускаем эту строку

            order = Order.objects.create(
                user=user,
                delivery_address=row.get('delivery_address', ''),
                promocode=row.get('promocode', ''),
            )

            product_ids = row.get('product_ids', '')
            if product_ids:
                product_ids_list = [pid.strip() for pid in product_ids.split(',') if pid.strip().isdigit()]
                products = Product.objects.filter(pk__in=product_ids_list)
                order.products.set(products)

            order.save()


# Представление для загрузки файла импорта заказов
def import_orders_view(request):
    if request.method == "POST":
        form = ImportOrdersForm(request.POST, request.FILES)
        if form.is_valid():
            import_file = form.cleaned_data['import_file']

            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    for chunk in import_file.chunks():
                        tmp_file.write(chunk)
                    tmp_filepath = tmp_file.name

                # Вызываем функцию импорта из файла CSV
                import_orders_from_file(tmp_filepath)

                messages.success(request, "Файл успешно загружен. Импорт заказов завершён.")
                return redirect('shopapp:orders_list')

            except Exception as e:
                messages.error(request, f"Ошибка при импорте: {e}")

    else:
        form = ImportOrdersForm()

    return render(request, "shopapp/import_orders.html", {"form": form})