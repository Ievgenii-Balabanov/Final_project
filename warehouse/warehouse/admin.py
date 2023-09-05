from django.contrib import admin

from .models import Book, BookItem, Category, Genre, Order, OrderItem, OrderItemBookItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'delivery_address', 'postal_code', 'city', 'payment',
                    'created_on', 'updated_on']
    list_filter = ['payment', 'created_on', 'updated_on']
    inlines = [OrderItemInline]


class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]


class BookItemAdmin(admin.ModelAdmin):
    list_display = ["name"]


class OrderItemBookItemAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemBookItem)
admin.site.register(Genre)

