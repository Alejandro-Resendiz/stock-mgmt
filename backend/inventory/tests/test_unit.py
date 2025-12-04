from faker import Faker
from django.test import TestCase

from inventory.utils import generate_unique_sku
from inventory.filters import ProductFilter
from inventory.serializers import StockTransferSerializer
from inventory.models import (
    Product,
    Store,
    Inventory
)


class ProductFilterTests(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.store = Store.objects.create(name='Test Store', city='Test City')
        self.p1 = Product.objects.create(
            name='Book A', category='Books', price=10.00,
            sku=generate_unique_sku(product={'category': 'Books'}, faker=self.faker)
        )
        self.p2 = Product.objects.create(
            name='Book B', category='Books', price=20.00,
            sku=generate_unique_sku(product={'category': 'Books'}, faker=self.faker)
        )
        self.p3 = Product.objects.create(
            name='Electronics C', category='Electronics', price=50.00,
            sku=generate_unique_sku(product={'category': 'Electronics'}, faker=self.faker)
        )
        
        Inventory.objects.create(product=self.p1, store=self.store, quantity=5, minStock=5)
        Inventory.objects.create(product=self.p2, store=self.store, quantity=0, minStock=5)

    def test_filter_by_category(self):
        queryset = Product.objects.all()
        filtered_qs = ProductFilter({'category': 'Books'}, queryset=queryset).qs
        self.assertEqual(filtered_qs.count(), 2)

    def test_filter_by_price_min(self):
        queryset = Product.objects.all()
        filtered_qs = ProductFilter({'price_min': 15.00}, queryset=queryset).qs
        self.assertEqual(filtered_qs.count(), 2)

    def test_filter_by_price_max(self):
        queryset = Product.objects.all()
        filtered_qs = ProductFilter({'price_max': 25.00}, queryset=queryset).qs
        self.assertEqual(filtered_qs.count(), 2)

    def test_filter_by_has_stock_true(self):
        queryset = Product.objects.all()
        filtered_qs = ProductFilter({'has_stock': 'true'}, queryset=queryset).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.p1)

    def test_filter_by_has_stock_false(self):
        queryset = Product.objects.all()
        filtered_qs = ProductFilter({'has_stock': 'false'}, queryset=queryset).qs
        self.assertEqual(filtered_qs.count(), 2)
        self.assertNotIn(self.p1, filtered_qs)


class StockTransferSerializerTests(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.product = Product.objects.create(
            name='Test Product', category='Test', price=10.0,
            sku=generate_unique_sku(product={'category': 'Test'}, faker=self.faker)
        )
        self.store1 = Store.objects.create(name='Store 1', city='Test City 1')
        self.store2 = Store.objects.create(name='Store 2', city='Test City 2')
        self.valid_data = {
            'product_id': str(self.product.id),
            'source_store_id': str(self.store1.id),
            'target_store_id': str(self.store2.id),
            'quantity': 10
        }

    def test_valid_data(self):
        serializer = StockTransferSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_same_stores(self):
        data = self.valid_data.copy()
        data['target_store_id'] = str(self.store1.id)
        serializer = StockTransferSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Cannot transfer products to the same store', serializer.errors['non_field_errors'][0])

    def test_invalid_data_zero_quantity(self):
        data = self.valid_data.copy()
        data['quantity'] = 0
        serializer = StockTransferSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

