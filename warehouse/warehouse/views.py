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


def dumpdata_api_view(request):
    book = Book.objects.all().values("id", "category", "name", "genre", "slug", "author", "image", "description",
                                     "price", "available", "created", "uploaded")
    category = Category.objects.all().values("id", "name", "slug")
    genre = Genre.objects.all().values("id", "name")

    category_list = list(category)
    book_list = list(book)
    genre_list = list(genre)
    return JsonResponse([book_list, category_list, genre_list], safe=False)


def order_create(request):
    if request.POST:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        delivery_address = request.POST.get("delivery_address")
        postal_code = request.POST.get("postal_code")
        city = request.POST.get("city")
        order = Order.objects.create(first_name=first_name, last_name=last_name, email=email,
                                     delivery_address=delivery_address, postal_code=postal_code, city=city)
        order.save()

        for item in cart:
            OrderItem.objects.create(order=order, book=item["product"], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'shop/orders/order/created.html',
                          {'order': order})


    else:
        return render(request, "shop/orders/order/create.html", {'cart': cart})
    return render(request, "shop/orders/order/create.html", {'cart': cart, 'order': order})

