from django.contrib import admin

from shop.models import Category, Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'delivery_address', 'postal_code', 'city', 'payment',
                    'created_on', 'updated_on']
    list_filter = ['payment', 'created_on', 'updated_on']
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
