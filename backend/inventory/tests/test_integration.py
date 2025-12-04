from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory.models import (
    Product,
    Store,
    Inventory
    # Movimiento
)

class ProductAPITests(APITestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Sample Product',
            'description': 'Description for sample product.',
            'category': 'Books',
            'price': '10.00',
            'sku': 'SKU-001'
        }
        self.product = Product.objects.create(**self.product_data)
        self.url_list = reverse('product-list-create')
        self.url_detail = reverse('product-detail', args=[str(self.product.id)])

    def test_list_products(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product(self):
        new_product_data = {
            'name': 'New Product',
            'description': 'New description.',
            'category': 'Electronics',
            'price': '99.99',
            'sku': 'SKU-002'
        }
        response = self.client.post(self.url_list, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Product')

    def test_update_product(self):
        updated_data = {
            **self.product_data,
            'name': 'Updated Name'
        }
        response = self.client.put(self.url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Name')

    def test_delete_product(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

class InventoryAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Widget',
            price=10,
            category='Tools',
            sku='SKU-003'
        )
        self.store1 = Store.objects.create(name='Store A', city='City A')
        self.store2 = Store.objects.create(name='Store B', city='City B')
        self.inventory1 = Inventory.objects.create(
            product=self.product, store=self.store1, quantity=100, minStock=10)
        self.inventory2 = Inventory.objects.create(
            product=self.product, store=self.store2, quantity=5, minStock=10)

    def test_store_inventory(self):
        url = reverse('store-inventory', args=[str(self.store1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quantity'], 100)

    def test_transfer_stock(self):
        url = reverse('transfer-stock')
        data = {
            'product_id': str(self.product.id),
            'source_store_id': str(self.store1.id),
            'target_store_id': str(self.store2.id),
            'quantity': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory1.refresh_from_db()
        self.inventory2.refresh_from_db()
        self.assertEqual(self.inventory1.quantity, 90)
        self.assertEqual(self.inventory2.quantity, 15)

    def test_transfer_to_same_store(self):
        url = reverse('transfer-stock')
        data = {
            'product_id': str(self.product.id),
            'source_store_id': str(self.store1.id),
            'target_store_id': str(self.store1.id),
            'quantity': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot transfer products to the same store', response.data['non_field_errors'][0])

    def test_transfer_insufficient_stock(self):
        url = reverse('transfer-stock')
        data = {
            'product_id': str(self.product.id),
            'source_store_id': str(self.store1.id),
            'target_store_id': str(self.store2.id),
            'quantity': 200
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough stock to transfer', response.data['error'])


    def test_inventory_alerts(self):
        url = reverse('inventory-alerts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['quantity'], 5)