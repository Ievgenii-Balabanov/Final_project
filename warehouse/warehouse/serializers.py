# from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Book, Category, Genre, Order, OrderItem

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = ["id", "category", "name", "genre", "author", "slug", "image", "description", "price", "available",
                  "created", "uploaded"]


# class BookItemSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = BookItem
#         fields = ["id", "book_id"]


class OrderItemSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    delivery_address = serializers.CharField()
    postal_code = serializers.CharField()
    city = serializers.CharField()
    created_on = serializers.DateTimeField()
    updated_on = serializers.DateTimeField()
    status = serializers.IntegerField()
    payment = serializers.BooleanField()
    shop_order_id = serializers.IntegerField()
    book_items = OrderItemSerializer(many=True)


# data = {
#     "id": id,
#     "first_name": "first_name",
#     "last_name": "last_name",
#     "email": "email",
#     "delivery_address": "delivery_address",
#     "postal_code": "postal_code",
#     "city": "city",
#     "created_on": "created_on",
#     "updated_on": "updated_on",
#     "payment": "payment",
#     "status": 0,
#     "shop_order_id": "id",
#     "book_items": [
#         {
#             "order_id": "item.book_id",
#             "book_id": "book_id",
#             "price": "item.price",
#             "quantity": "item.quantity"}
#         # } for item in order.items.all()
#     ],
# }
#
# serializer = OrderSerializer(data=data)
# if serializer.is_valid():
#     serialized_data = serializer.validated_data
#     print(serialized_data)
#
# print(serializer.errors)


# class OrderItemBookItemSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = OrderItemBookItem
#         fields = ["id", "order_item_id", "book_item_id"]

