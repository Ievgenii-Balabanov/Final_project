import django
import requests
from django.conf import settings

from celery import shared_task
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse

from shop.models import Category, Genre, Product, Order

django.setup()


@shared_task
def add_new_genre():
    while True:
        warehouse = "http://127.0.0.1:8001/json_dumpdata"
        json_result = requests.get(warehouse).json()
        for item in json_result[2]:
            name = item['name']
            id = item["id"]
            if not Genre.objects.filter(id=id).exists():
                new = Genre.objects.create(id=id, name=name)


@shared_task
def add_new_category():
    while True:
        warehouse = "http://127.0.0.1:8001/json_dumpdata"
        json_result = requests.get(warehouse).json()
        for item in json_result[1]:
            name = item['name']
            slug = item['slug']
            id = item["id"]
            if not Category.objects.filter(id=id).exists():
                new = Category.objects.create(id=id, name=name, slug=slug)


@shared_task
def add_new_books():
    while True:
        warehouse = "http://127.0.0.1:8001/json_dumpdata"
        json_result = requests.get(warehouse).json()
        for item in json_result[0]:
            name = item['name']
            category = Category.objects.get(id=item['category'])
            author = item['author']
            slug = item['slug']
            image = item['image']
            description = item['description']
            price = item['price']
            available = item['available']
            created = item['created']
            uploaded = item['uploaded']
            id_in_warehouse = item['id']
            if not Product.objects.filter(id_in_warehouse=id_in_warehouse).exists():
                if available:
                    new = Product.objects.create(category=category, name=name, author=author, slug=slug, image=image,
                                                 description=description, price=price, available=available,
                                                 created=created, uploaded=uploaded, id_in_warehouse=id_in_warehouse)
                    new.genre.add(Genre.objects.get(id=item['genre']))


@shared_task
def send_email(subject, message, from_email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, [from_email])


@shared_task
def add_order_to_warehouse(id_: int):
    order = Order.objects.get(pk=id_)
    data = {
        "first_name": order.first_name,
        "last_name": order.last_name,
        "email": order.email,
        "delivery_address": order.delivery_address,
        "postal_code": order.postal_code,
        "city": order.city,
        "created_on": str(order.created_on),
        "updated_on": str(order.updated_on),
        "payment": order.payment,
        "status": 0,
        "shop_order_id": order.pk,
        "book_items": [
            {
                "warehouse_book_id": item.book_id,
                "price": str(item.price),
                "quantity": item.quantity
            } for item in order.items.all()
        ],
    }
    requests.post("http://127.0.0.1:8001/create_order/", json=data)



    # order = serialize("json", order_id)
    # url = "http://localhost:8001/create_order/"
    # order_for_api = requests.post(url, json=order)



# @shared_task
# def warehouse_bookshelf_update():
#     pass
3
    # shop_orders = "http://127.0.0.1:8000/warehouse_new_order/"
    # json_result = requests.get(shop_orders).json()
    #
    # for order in json_result:
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
