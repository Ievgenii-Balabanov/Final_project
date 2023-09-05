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


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "first_name", "last_name", "email", "delivery_address", "postal_code", "city",
                  "created_on", "updated_on", "status", "payment"]


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["id", "order_id", "book_id", "price", "quantity"]


class OrderItemBookItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrderItemBookItem
        fields = ["id", "order_item_id", "book_item_id"]

