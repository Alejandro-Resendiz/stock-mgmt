import django_filters
from rest_framework.pagination import PageNumberPagination

from .models import Product


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category", lookup_expr='iexact')
    has_stock = django_filters.BooleanFilter(method='filter_has_stock')

    def filter_has_stock(self, queryset, name, value):
        if value:
            return queryset.filter(products_inventory__quantity__gt=0).distinct()
        else:
            return queryset.exclude(products_inventory__quantity__gt=0).distinct()

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max']