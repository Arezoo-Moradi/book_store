from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Address


# Create your tests here.
class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='john',
            email='john@gmail.com',
            password='jj123456'
        )
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AddressTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='secret'
        )
        self.address = Address.objects.create(
            province='A good title',
            city='Nice body content',
            full_address='just for test',
            postal_code='123456',
            user=self.user
        )

    def test_post_content(self):
        self.assertEqual(f'{self.address.province}', 'A good title')
        self.assertEqual(f'{self.address.user}', 'test@gmail.com')
        self.assertEqual(f'{self.address.city}', 'Nice body content')
