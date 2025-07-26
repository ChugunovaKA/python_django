from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from shopapp.models import Order, Product  # замените на ваши модели, если отличаются


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='pass1234')
        # Добавляем нужные права на просмотр заказа
        permission = Permission.objects.get(codename='view_order')  # 'shopapp.view_order'
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        # Вход пользователя
        self.client = Client()
        self.client.login(username='testuser', password='pass1234')
        # Создаем тестовый заказ (примитивный пример, адаптируйте под вашу модель)
        self.order = Order.objects.create(
            address='123 Test St',
            promocode='PROMO2025',
            user=self.user
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        url = reverse('order_detail', args=[self.order.pk])  # проверьте имя url и аргументы
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в теле ответа есть адрес и промокод
        self.assertIn(self.order.address, response.content.decode())
        self.assertIn(self.order.promocode, response.content.decode())

        # Проверяем, что в контексте тот же заказ
        self.assertEqual(response.context['order'].pk, self.order.pk)