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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Обычный пользователь без прав staff
        cls.user = User.objects.create_user(username='regularuser', password='userpass')

        # Staff пользователь с правами
        cls.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.staff_user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=9.99,
            discount=0,
            archived=False,
        )

        # Создаем заказ, связанный со staff пользователем
        self.order = Order.objects.create(
            delivery_address='Test Address',
            promocode='PROMO',
            user=self.staff_user,
        )
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_access_requires_staff(self):
        # Без авторизации - доступ запрещён (обычно 302 редирект на логин)
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertNotEqual(response.status_code, 200)

        # Залогинен обычный пользователь - доступ запрещён
        self.client.login(username='regularuser', password='userpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()

        # Залогинен staff-пользователь - доступ разрешён
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)

        # Проверяем JSON-структуру и данные
        data = response.json()
        self.assertIn("orders", data)
        self.assertTrue(isinstance(data["orders"], list))
        self.assertGreaterEqual(len(data["orders"]), 1)

        # Проверяем поля первого заказа
        order_data = data["orders"][0]
        self.assertEqual(order_data["id"], self.order.id)
        self.assertEqual(order_data["delivery_address"], self.order.delivery_address)
        self.assertEqual(order_data["promocode"], self.order.promocode)
        self.assertEqual(order_data["user_id"], self.staff_user.id)
        self.assertIn(self.product.id, order_data["product_ids"])

        self.client.logout()