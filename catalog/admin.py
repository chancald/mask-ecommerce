from django.contrib import admin
from .models import Item, Order, OrderItem, Address, Promo

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = [
        'title',
        'price',
        'discount_price'
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
    'street_address',
    'street_address_2',
    'default',
    'state_option',
    'payment_option'
    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Promo)
admin.site.register(Order)
admin.site.register(OrderItem)