from django.test import TestCase
from django.test import TestCase
from .models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name='داستان')

        def test_text_content(self):
            cat = Category.objects.get(id=1)
            expected_object_name = f'{cat.name}'
            self.assertEqual(expected_object_name, 'داستان')