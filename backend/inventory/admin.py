from django.contrib import admin

from .models import (
    Product,
    Store,
    Inventory,
    Movement
)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'quantity', 'minStock')
    list_filter = ('store', 'product')
    search_fields = ('product__name', 'store__name') 

admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Movement)

