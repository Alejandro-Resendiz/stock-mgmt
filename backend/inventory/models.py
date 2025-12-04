import uuid
from django.db import models

MOVEMENT_IN = 'IN'
MOVEMENT_OUT = 'OUT'
MOVEMENT_TRANSFER = 'TRANSFER'
MOVEMENT_TYPE_CHOICES = (
    (MOVEMENT_IN, 'In'),
    (MOVEMENT_OUT, 'Out'),
    (MOVEMENT_TRANSFER, 'Transfer')
)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'name'])
        ]


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
        ]


class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, related_name='products_inventory',
        on_delete=models.CASCADE, db_index=True
    )
    store = models.ForeignKey(
        Store, related_name='store_inventory',
        on_delete=models.CASCADE, db_index=True
    )
    quantity = models.IntegerField()
    minStock = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.store}"

    class Meta:
        unique_together = ('product', 'store')
        indexes = [
            models.Index(fields=['product', 'store'])
        ]


class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    sourceStore = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='movements_out', null=True
    )
    targetStore =  models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='movements_in', null=True
    )
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    type = models.CharField(choices=MOVEMENT_TYPE_CHOICES, db_index=True)

    def __str__(self):
        return f"{self.type} {self.quantity} <{self.product}> FROM <{self.sourceStore}> TO <{self.targetStore}>"

    class Meta:
        indexes = [
            models.Index(fields=['product', '-timestamp']),
            models.Index(fields=['type', '-timestamp']),
            models.Index(fields=['sourceStore', 'targetStore']),
        ]
