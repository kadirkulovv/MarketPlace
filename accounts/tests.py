from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_buyer_user(self):
        user = User.objects.create_user(
            username='test_buyer',
            email='buyer@test.com',
            password='TestPassword123!',
            role='buyer'
        )
        self.assertEqual(user.username, 'test_buyer')
        self.assertTrue(user.is_buyer)
        self.assertFalse(user.is_seller)
        self.assertFalse(user.is_staff)

    def test_create_seller_user(self):
        user = User.objects.create_user(
            username='test_seller',
            email='seller@test.com',
            password='TestPassword123!',
            role='seller',
            shop_name='SuperStore'
        )
        self.assertTrue(user.is_seller)
        self.assertFalse(user.is_buyer)
        self.assertEqual(user.shop_name, 'SuperStore')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin_user',
            email='admin@test.com',
            password='AdminPassword123!'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
