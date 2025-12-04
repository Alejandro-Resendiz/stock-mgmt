from rest_framework import serializers
from .models import (
    Product,
    Store,
    Inventory,
    Movement
)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ['id']

class InventoryListSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    # store = StoreSerializer(read_only=True)
    
    class Meta:
        model = Inventory
        fields = '__all__'

class MovementSerializer(serializers.ModelSerializer):
    type_display = serializers.SerializerMethodField()

    def get_type_display(self, obj):
        return obj.get_type_display()

    class Meta:
        model = Movement
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

class StockTransferSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    source_store_id = serializers.UUIDField()
    target_store_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        if data['source_store_id'] == data['target_store_id']:
            raise serializers.ValidationError("Cannot transfer products to the same store.")
        return data