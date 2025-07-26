from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from shopapp.models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='pass1234')
        # Добавляем право на просмотр заказа
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        # Логинимся клиентом
        self.client = Client()
        logged_in = self.client.login(username='testuser', password='pass1234')
        self.assertTrue(logged_in, "Не удалось выполнить вход пользователя в тесте")

        # Создаем продукт
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=10.00,
            discount=0,
            archived=False
        )

        # Создаем заказ
        self.order = Order.objects.create(
            delivery_address='123 Test St',
            promocode='PROMO2025',
            user=self.user
        )
        # Добавляем продукт к заказу
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        url = reverse('shopapp:order_details', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в ответе есть адрес и промокод
        response_content = response.content.decode()
        self.assertIn(self.order.delivery_address, response_content)
        self.assertIn(self.order.promocode, response_content)

        # Проверяем, что в контексте тот же заказ
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportViewTestCase(TestCase):
    fixtures = ['test_data.json']  # укажите имя вашего файла фикстур

    @classmethod
    def setUpTestData(cls):
        # Получаем пользователей, которые загружаются из фикстур
        cls.regular_user = User.objects.get(username='regularuser')
        cls.staff_user = User.objects.get(username='staffuser')

        # Устанавливаем их пароли заново, чтобы логин сработал
        cls.regular_user.set_password('userpass')
        cls.regular_user.save()
        cls.staff_user.set_password('staffpass')
        cls.staff_user.save()

    def setUp(self):
        self.client = Client()

    def test_access_requires_staff(self):
        # Без авторизации - доступ запрещён
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertNotEqual(response.status_code, 200)

        # Авторизация обычным пользователем - доступ запрещён
        self.client.login(username='regularuser', password='userpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()

        # Авторизация staff пользователем - доступ разрешён
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)

        # Получаем JSON из ответа
        response_data = response.json()

        # Формируем ожидаемые данные из базы
        orders = Order.objects.select_related('user').prefetch_related('products').all()

        expected_orders_data = []
        for order in orders:
            expected_orders_data.append({
                "id": order.id,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.id,
                "product_ids": list(order.products.values_list('id', flat=True))
            })

        expected_data = {"orders": expected_orders_data}

        # Сравниваем всю структуру целиком
        self.assertEqual(response_data, expected_data)

        self.client.logout()