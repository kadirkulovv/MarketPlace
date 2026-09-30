from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Order, OrderItem

User = get_user_model()

class OrderModuleTest(TestCase):
    def test_order_creation_and_stock_reduction(self):
        seller = User.objects.create_user(username='seller_o', email='so@test.com', password='Pass!', role='seller')
        buyer = User.objects.create_user(username='buyer_o', email='bo@test.com', password='Pass!', role='buyer')
        cat = Category.objects.create(name='Kitoblar')
        product = Product.objects.create(
            seller=seller, category=cat, name='Python Asoslari', price=100000, stock=10
        )

        order = Order.objects.create(
            user=buyer, full_name='Eshmat Toshmatov', phone='+998901112233', address='Toshkent'
        )
        OrderItem.objects.create(
            order=order, product=product, price=product.current_price, quantity=3
        )
        product.stock -= 3
        product.save()

        product.refresh_from_db()
        self.assertEqual(order.total_cost, 300000)
        self.assertEqual(product.stock, 7)
        self.assertEqual(product.total_sold(), 3)
