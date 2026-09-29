from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product

User = get_user_model()

class ProductModuleTest(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller1', email='s1@test.com', password='Password123!', role='seller'
        )
        self.cat_main = Category.objects.create(name='Elektronika')
        self.cat_sub = Category.objects.create(name='Telefonlar', parent=self.cat_main)
        self.cat_child = Category.objects.create(name='Smartfonlar', parent=self.cat_sub)

        self.product = Product.objects.create(
            seller=self.seller,
            category=self.cat_child,
            name='iPhone 15',
            description='Yangi smartfon',
            price=12000000,
            discount_price=11000000,
            stock=15
        )

    def test_category_mptt_hierarchy(self):
        descendants = list(self.cat_main.get_descendants(include_self=True))
        self.assertEqual(len(descendants), 3)
        self.assertIn(self.cat_child, descendants)

    def test_product_price_and_slug(self):
        self.assertEqual(self.product.slug, 'iphone-15')
        self.assertEqual(self.product.current_price, 11000000)
        self.assertTrue(self.product.is_in_stock)

    def test_category_products_filter(self):
        # Ota kategoriya orqali qidirganda ham bola kategoriyadagi mahsulot chiqishi kerak
        cats = self.cat_main.get_descendants(include_self=True)
        prods = Product.objects.filter(category__in=cats)
        self.assertEqual(prods.count(), 1)
