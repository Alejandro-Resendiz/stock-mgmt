import random
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from itertools import chain
from math import floor

from inventory.utils import generate_unique_sku
from inventory.models import (
    Inventory,
    Product,
    Store
)


class Command(BaseCommand):
    help = 'Create random stores, products and inventory for each store'

    def add_arguments(self, parser):
        parser.add_argument('num_products', type=int, help='Number of products to create')
        parser.add_argument('num_stores', type=int, help='Number of stores to create')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        num_products = kwargs['num_products']
        num_stores = kwargs['num_stores']
        fake = Faker()

        self.stdout.write("Creating data...")

        stores_to_create = [
            Store(
                name=fake.unique.company(),
                address=fake.address(),
                city=fake.city()
            ) for _ in range(num_stores)
        ]
        new_stores = Store.objects.bulk_create(stores_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_stores} stores."))

        response = requests.get('https://fakestoreapi.com/products')
        fake_products = response.json()[:num_products]

        products_to_create = [
            Product(
                name=item['title'],
                description=item['description'],
                category=item['category'],
                price=item['price'],
                sku=generate_unique_sku(product=item,faker=fake)
            ) for item in fake_products
        ]
        new_products = Product.objects.bulk_create(products_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_products} products."))

        inventory_by_store = [
            [
                Inventory(
                    product=new_product,
                    store=new_store,
                    quantity=floor(random.uniform(10.0, 101.0)),
                    minStock=random.choice([5, 10, 15, 20])
                )
                for new_product in new_products
            ] for new_store in new_stores
        ]
        inventory_iterator = chain.from_iterable(inventory_by_store)
        inventory_to_create = list(inventory_iterator)
        Inventory.objects.bulk_create(inventory_to_create)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_products * num_stores} inventory items."))
