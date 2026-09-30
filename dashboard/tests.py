from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Category, Product

User = get_user_model()

class DashboardModuleTest(TestCase):
    def test_seller_vs_buyer_permission(self):
        buyer = User.objects.create_user(username='b_user', email='b@t.com', password='Password123!', role='buyer')
        seller = User.objects.create_user(username='s_user', email='s@t.com', password='Password123!', role='seller')

        # Xaridor kirsa ruxsat berilmasligi kerak (403)
        self.client.login(username='b_user', password='Password123!')
        response = self.client.get(reverse('dashboard:seller_dashboard'))
        self.assertEqual(response.status_code, 403)

        # Sotuvchi kirsa sahifa ochilishi kerak (200 yoki template)
        self.client.login(username='s_user', password='Password123!')
        response = self.client.get(reverse('dashboard:seller_products'))
        self.assertEqual(response.status_code, 200)

class SellerDashboardLogicTest(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='s_user', email='s@t.com', password='Password123!', role='seller')
        self.buyer = User.objects.create_user(username='b_user', email='b@t.com', password='Password123!', role='buyer')
        self.cat = Category.objects.create(name='Test')

        # Sotuvchining mahsulotlari va buyurtmalari
        p1 = Product.objects.create(seller=self.seller, name='Test Product 1', stock=10, price=1000, category=self.cat)
        p2 = Product.objects.create(seller=self.seller, name='Test Product 2', stock=0, price=2000, category=self.cat)

        o1 = Order.objects.create(user=self.buyer, full_name='Test Buyer')
        OrderItem.objects.create(order=o1, product=p1, quantity=2, price=1000)
        OrderItem.objects.create(order=o1, product=p2, quantity=1, price=2000)

    def test_stock_update_view(self):
        self.client.login(username='s_user', password='Password123!')
        response = self.client.post(
            reverse('dashboard:update_stock', args=[Product.objects.first().pk]),
            {'stock': '5'}
        )
        updated_product = Product.objects.first()
        self.assertEqual(updated_product.stock, 5)
        self.assertRedirects(response, reverse('dashboard:seller_products'))

    def test_seller_products_view(self):
        self.client.login(username='s_user', password='Password123!')
        response = self.client.get(reverse('dashboard:seller_products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)

    def test_seller_orders_view(self):
        self.client.login(username='s_user', password='Password123!')
        response = self.client.get(reverse('dashboard:seller_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order_items'].count(), 2)

    def test_seller_dashboard_view(self):
        self.client.login(username='s_user', password='Password123!')
        response = self.client.get(reverse('dashboard:seller_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_product_update_delete_view(self):
        self.client.login(username='s_user', password='Password123!')
        prod = Product.objects.filter(seller=self.seller).first()

        # Tahrirlash
        response = self.client.post(reverse('dashboard:product_update', args=[prod.pk]), {
            'name': prod.name, 'stock': 10, 'price': prod.price, 'category': prod.category.pk
        })
        self.assertEqual(response.status_code, 302)

        # O'chirish
        response = self.client.post(reverse('dashboard:product_delete', args=[prod.pk]))
        self.assertEqual(response.status_code, 302)
