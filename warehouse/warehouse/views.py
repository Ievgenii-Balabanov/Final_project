from django.http import JsonResponse
from rest_framework import request, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, Category, Genre, Order, OrderItem
from .serializers import CategorySerializer, GenreSerializer, BookSerializer, OrderSerializer


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


@api_view(['GET', 'POST'])
def create_order(request):
    print("Hello")
    if request.method == 'GET':
        orders = Order.objects.all()
        print("GET")
        serializer = OrderSerializer(orders)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("POST")
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer is Valid")
            print(serializer.data.get("shop_order_id"))
            print(serializer.data.items())
            order = Order.objects.create(
                first_name=serializer.data.get("first_name"),
                last_name=serializer.data.get("last_name"),
                email=serializer.data.get("email"),
                status=serializer.data.get("status"),
                delivery_address=serializer.data.get("delivery_address"),
                postal_code=serializer.data.get("postal_code"),
                city=serializer.data.get("city"),
                created_on=serializer.data.get("created_on"),
                updated_on=serializer.data.get("updated_on"),
                payment=serializer.data.get("payment"),
                shop_order_id=serializer.data.get("shop_order_id")
            )

            for item in request.data.get("book_items"):
                book = Book.objects.get(pk=item.get("book_id"))
                order_item = OrderItem.objects.create(
                    order_id=order, book_id=book, price=item.get("price"),
                    quantity=item.get("quantity")
                )

                book = Book.objects.get(pk=item.get("book_id"))
                book.available = False
                book.save()

            return Response(status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
