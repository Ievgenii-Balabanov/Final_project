import json

import requests
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from rest_framework import request, viewsets, status
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

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


# ------------------------------------------------------------------
# @api_view(['GET', 'POST'])
# def create_order(request):
#     print("Hello")
#     if request.method == 'GET':
#         snippets = Order.objects.all()
#         print("GET")
#         serializer = OrderSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.POST:
#         print("POST")
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             print("No")
#             order = Order.objects.create(
#                 first_name=serializer.data.get("first_name"), last_name=serializer.data.get("last_name"),
#                 email=serializer.data.get("email"),
#                 status=serializer.data.get("status"),
#                 delivery_address=serializer.data.get("delivery_address"), postal_code=serializer.data.get("postal_code"),
#                 city=serializer.data.get("city"),
#                 created_on=serializer.data.get("created_on"), updated_on=serializer.data.get("updated_on"),
#                 payment=serializer.data.get("payment"),
#                 shop_order_id=serializer.data.get("shop_order_id")
#             )
#             serializer.save()
#
#             for item in request.data.get("book_items"):
#                 order_item = OrderItem.objects.create(
#                     order_id=order.pk, book_id=item.get("warehouse_book_id"), price=item.get("price"),
#                     quantity=item.get("quantity")
#                 )
#
#                 book = Book.objects.get(pk=item.get("warehouse_book_id"))
#                 book.available = False
#                 book.save()
#
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#             # data = json.loads(serializer)
#             # order = Order.objects.create(
#             #     first_name=serializer.data("first_name"), last_name=serializer.data("last_name"), email=serializer.data("email"),
#             #     status=serializer.data("status"),
#             #     delivery_address=serializer.data("delivery_address"), postal_code=serializer.data("postal_code"),
#             #     city=serializer.data("city"),
#             #     created_on=serializer.data("created_on"), updated_on=serializer.data("updated_on"), payment=serializer.data("payment"),
#             #     shop_order_id=serializer.data("shop_order_id")
#             # )
#         #     for item in request.data.get("book_items"):
#         #         order_item = OrderItem.objects.create(
#         #             order_id=order.pk, book_id=item.get("warehouse_book_id"), price=item.get("price"),
#         #             quantity=item.get("quantity")
#         #         )
#         #
#         #         book = Book.objects.get(pk=item.get("warehouse_book_id"))
#         #         book.available = False
#         #         book.save()
#         #     else:
#         #         return Response(serializer.errors)
#         # context = {'data': serializer.data}
#         # return Response(context)

    # ------------------------------------------------------------------

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
            # Order.objects.save()
            for item in request.data.get("book_items"):
                book = Book.objects.get(pk=item.get("book_id"))
                order_item = OrderItem.objects.create(
                    # order_id=order.pk, book_id=item.get("book_id"), price=item.get("price"),
                    order_id=order, book_id=book, price=item.get("price"),
                    quantity=item.get("quantity")
                )

                book = Book.objects.get(pk=item.get("book_id"))
                book.available = False
                book.save()
            print("No")
            return Response(order, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)






    # body_unicode = request.body.decode('utf-8')
    # data = json.loads(request.body)
    # first_name = data['first_name']
    # last_name = data['last_name']
    # email = data['email']
    # delivery_address = data['delivery_address']
    # postal_code = data['postal_code']
    # city = data['city']
    # created_on = data['created_on']
    # updated_on = data['updated_on']
    # payment = data['payment']
    # status = data['status']
    # shop_order_id = data['id']
    #
    # Order.objects.create(first_name=first_name, last_name=last_name, email=email, status=status,
    #                      delivery_address=delivery_address, postal_code=postal_code, city=city, created_on=created_on,
    #                      updated_on=updated_on, payment=payment, shop_order_id=shop_order_id)
    #
    # available_status = Book.objects.update(available=False)

        # first_name = request.POST.get("first_name")
        # last_name = request.POST.get("last_name")
        # email = request.POST.get("email")
        # delivery_address = request.POST.get("delivery_address")
        # postal_code = request.POST.get("postal_code")
        # city = request.POST.get("city")
        # created_on = request.POST.get("created_on")
        # updated_on = request.POST.get("updated_on")
        # payment = request.POST.get("payment")
        # status = request.POST.get("status")
        # shop_order_id = request.POST.get("id")

        # if not Order.objects.filter(shop_order_id=order.shop_order_id).exists():
        # new_order = Order.objects.create(first_name=first_name, last_name=last_name, email=email,
        #                                  status=status,
        #                                  delivery_address=delivery_address, postal_code=postal_code,
        #                                  city=city,
        #                                  created_on=created_on, updated_on=updated_on,
        #                                  payment=payment,
        #                                  shop_order_id=shop_order_id)

    # shop_orders = "http://127.0.0.1:8000/warehouse_new_order/"
    # json_result = requests.get(shop_orders).json()
    #
    # for order in json_result[0]:
    #     first_name = order["first_name"]
    #     last_name = order["last_name"]
    #     email = order["email"]
    #     delivery_address = order["delivery_address"]
    #     postal_code = order["postal_code"]
    #     city = order["city"]
    #     created_on = order["created_on"]
    #     updated_on = order["updated_on"]
    #     payment = order["payment"]
    #     status = 0
    #     shop_order_id = order["id"]
    #
    #     if not Order.objects.filter(shop_order_id=shop_order_id).exists():
    #         new_order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, status=status,
    #                                          delivery_address=delivery_address, postal_code=postal_code, city=city,
    #                                          created_on=created_on, updated_on=updated_on, payment=payment,
    #                                          shop_order_id=shop_order_id)
