import json

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets

from .models import Book, BookItem, Category, Genre, Order, OrderItem, OrderItemBookItem
from .serializers import CategorySerializer, GenreSerializer, BookSerializer, BookItemSerializer, OrderSerializer, \
    OrderItemSerializer, OrderItemBookItemSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Book model.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for "Category" model.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset provides 'list', 'create', 'retrieve',
    `update` and `destroy` actions for "Genre" model.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def perform_create(self, serializer):
        serializer.save()


# class BookViewSet(viewsets.ModelViewSet):
#     """
#     Viewset provides 'list', 'create', 'retrieve',
#     `update` and `destroy` actions for "Genre" model.
#     """
#
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#
#     def perform_create(self, serializer):
#         serializer.save()

# def dumpdata_api_view(request):
#     books = serialize("json", Book.objects.all())
#     categories = serialize("json", Category.objects.all())
#     genres = serialize("json", Genre.objects.all())
#
#     return JsonResponse({
#         "books": books,
#         "categories": categories,
#         "genres": genres
#     }, safe=False)

# def dumpdata_api_view(request):
    # books = serialize("json", Book.objects.all())
    # categories = serialize("json", Category.objects.all())
    # genres = serialize("json", Genre.objects.all())

    # return JsonResponse({"categories": categories})

def dumpdata_api_view(request):
    book = Book.objects.all().values("id", "category", "name", "genre", "slug", "author", "image", "description",
                                     "price", "available", "created", "uploaded")
    category = Category.objects.all().values("id", "name", "slug")
    genre = Genre.objects.all().values("id", "name")

    category_list = list(category)
    book_list = list(book)
    genre_list = list(genre)
    return JsonResponse([book_list, category_list, genre_list], safe=False)
