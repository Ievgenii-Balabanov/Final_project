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
    books = Genre.objects.all()
    books.delete()
    warehouse = "http://127.0.0.1:8001/json_dumpdata"
    json_result = requests.get(warehouse).json()
    for item in json_result[2]:
        name = item['name']
        id = item["id"]
        if not Genre.objects.filter(id=id).exists():
            new = Genre.objects.create(id=id, name=name)


@shared_task
def add_new_category():
    books = Category.objects.all()
    books.delete()
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

        ids = []
        for element in json_result[0]:
            ids.append(element['id'])
        queryset = Product.objects.filter(id_in_warehouse__in=ids)
        for book in queryset:
            book.available = item["available"]
            # Product.objects.all().update(available=available)
            book.save()

        if not Product.objects.filter(id_in_warehouse=id_in_warehouse).exists():
            new = Product.objects.create(category=category, name=name, author=author, slug=slug, image=image,
                                         description=description, price=price, available=available,
                                         created=created, uploaded=uploaded, id_in_warehouse=id_in_warehouse)
            new.genre.add(Genre.objects.get(id=item['genre']))


@shared_task
def send_email(subject, message, from_email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, [from_email])


@shared_task
def contact_us_email(subject, message, email):
    send_mail(subject, message, settings.NOREPLY_EMAIL, [email])


@shared_task
def add_order_to_warehouse(id_: int):
    order = Order.objects.get(pk=id_)
    print(order)
    print(order.pk)
    data = {
        "first_name": order.first_name,
        "last_name": order.last_name,
        "email": order.email,
        "delivery_address": order.delivery_address,
        "postal_code": order.postal_code,
        "city": order.city,
        "created_on": str(order.created_on),
        "updated_on": str(order.updated_on),
        # "payment": order.payment,
        "payment": 0,
        "status": 0,
        "shop_order_id": order.pk,
        "book_items": [
            {
                "order_id": item.pk,
                "book_id": item.book.id_in_warehouse,
                "price": str(item.price),
                "quantity": item.quantity,
            } for item in order.items.all()
        ],
    }
    print(f'Id is {data["shop_order_id"]}')
    requests.post("http://127.0.0.1:8001/create_order/", json=data)
    print(data)
