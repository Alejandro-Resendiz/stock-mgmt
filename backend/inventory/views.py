from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from django.db import transaction

from .filters import ProductFilter, StandardPagination
from .models import (
    Product,
    Store,
    Inventory,
    Movement,
    MOVEMENT_TRANSFER
)
from .serializers import (
    ProductSerializer,
    InventoryListSerializer,
    StockTransferSerializer,
    StoreSerializer
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('name') 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = StandardPagination

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
 

class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all().order_by('name') 
    serializer_class = StoreSerializer
    pagination_class = StandardPagination


@api_view(['GET'])
def store_inventory(request, store_id):
    try:
        store = Store.objects.get(pk=store_id)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
    
    inventory = Inventory.objects.filter(store=store)
    serializer = InventoryListSerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def transfer_stock(request):
    serializer = StockTransferSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    product_id = validated_data['product_id']
    source_store_id = validated_data['source_store_id']
    target_store_id = validated_data['target_store_id']
    quantity = validated_data['quantity']

    try:
        with transaction.atomic():
            product = Product.objects.get(pk=product_id)
            source_store = Store.objects.get(pk=source_store_id)
            target_store = Store.objects.get(pk=target_store_id)

            source_inventory = Inventory.objects.get(product=product, store=source_store)
            target_inventory, _ = Inventory.objects.get_or_create(
                product=product,
                store=target_store,
                defaults={'quantity': 0, 'minStock': 0})

            if source_inventory.quantity < quantity:
                return Response(
                    {'error': 'Not enough stock to transfer.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            source_inventory.quantity = F('quantity') - quantity
            target_inventory.quantity = F('quantity') + quantity
            source_inventory.save()
            target_inventory.save()

            Movement.objects.create(
                product=product,
                sourceStore=source_store,
                targetStore=target_store,
                quantity=quantity,
                type=MOVEMENT_TRANSFER
            )
        
        return Response({'message': 'Transfer successful'}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def inventory_alerts(request):
    low_stock_items = Inventory.objects.filter(quantity__lt=F('minStock'))
        # .select_related('product', 'store')
    serializer = InventoryListSerializer(low_stock_items, many=True)
    return Response(serializer.data)
