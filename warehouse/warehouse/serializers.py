# from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Book, BookItem, Category, Genre, Order, OrderItem, OrderItemBookItem


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


class BookItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BookItem
        fields = ["id", "book_id"]


# class OrderSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = ["id", "first_name", "last_name", "email", "delivery_address", "postal_code", "city",
#                   "created_on", "updated_on", "status", "payment"]

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ["id", "first_name", "last_name", "email", "delivery_address", "postal_code", "city",
#                   "created_on", "updated_on", "status", "payment"]


class OrderItemSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
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
    book_items = OrderItemSerializer(many=True)


# class OrderItemSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = OrderItem
#         fields = ["id", "order_id", "book_id", "price", "quantity"]
#
#
class OrderItemBookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemBookItem
        fields = ["id", "order_item_id", "book_item_id"]

