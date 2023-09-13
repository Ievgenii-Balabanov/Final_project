import django
import requests
from django.conf import settings

from celery import shared_task
from django.core.mail import send_mail

from warehouse.models import Order, OrderItem, Book, OrderItemBookItem

django.setup()


# @shared_task
# def warehouse_bookshelf_update():
#     shop_orders = "http://127.0.0.1:8000/warehouse_new_order/"
#     json_result = requests.get(shop_orders).json()
#
#     for order in json_result[0]:
#         first_name = order["first_name"]
#         last_name = order["last_name"]
#         email = order["email"]
#         delivery_address = order["delivery_address"]
#         postal_code = order["postal_code"]
#         city = order["city"]
#         created_on = order["created_on"]
#         updated_on = order["updated_on"]
#         payment = order["payment"]
#         status = 0
#         shop_order_id = order["id"]
#
#         if not Order.objects.filter(shop_order_id=shop_order_id).exists():
#             new_order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, status=status,
#                                              delivery_address=delivery_address, postal_code=postal_code, city=city,
#                                              created_on=created_on, updated_on=updated_on, payment=payment,
#                                              shop_order_id=shop_order_id)


@shared_task
def add_order():
    shop_orders = "http://127.0.0.1:8000/warehouse_new_order/"
    json_result = requests.get(shop_orders).json()

    for order in json_result[0]:
        first_name = order["first_name"]
        last_name = order["last_name"]
        email = order["email"]
        delivery_address = order["delivery_address"]
        postal_code = order["postal_code"]
        city = order["city"]
        created_on = order["created_on"]
        updated_on = order["updated_on"]
        payment = order["payment"]
        status = 0
        shop_order_id = order["id"]

        if not Order.objects.filter(shop_order_id=shop_order_id).exists():
            Order.objects.create(first_name=first_name, last_name=last_name, email=email, status=status,
                                 delivery_address=delivery_address, postal_code=postal_code, city=city,
                                 created_on=created_on, updated_on=updated_on, payment=payment,
                                 shop_order_id=shop_order_id)

            for item in json_result[1]:
                order_id = Order.objects.get(id=item["id"])
                book_id = Book.objects.get(id=item["book"])
                price = item["price"]
                quantity = item["quantity"]
                if not OrderItem.objects.filter(order_id=order_id).exists():
                    OrderItem.objects.create(order_id=order_id, book_id=book_id, price=price, quantity=quantity)


# @shared_task
# def add_order_item():
#     shop_orders = "http://127.0.0.1:8000/warehouse_new_order/"
#     json_result = requests.get(shop_orders).json()
#
#     for item in json_result[1]:
#         order_id = Order.objects.get(id=item["id"])
#         book_id = Book.objects.get(id=item["book"])
#         price = item["price"]
#         quantity = item["quantity"]
#         if not OrderItem.objects.filter(order_id=order_id).exists():
#             OrderItem.objects.create(order_id=order_id, book_id=book_id, price=price, quantity=quantity)
#
#                 # OrderItemBookItem.objects.create(order_item_id=order_id, book_item_id=book_id)
