import django
import requests

from celery import shared_task
# from django.conf import settings

from shop.models import Category, Genre, Product

# django.setup()

#
# @shared_task
# def add(x, y):
#     return x + y


@shared_task
def add_new_books():
    while True:
        warehouse = "http://127.0.0.1:8001/json_dumpdata"
        json_result = requests.get(warehouse).json()
        # current_books = "http://127.0.0.1:8000/book/"
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
                new = Product.objects.create(category=category, name=name, author=author, slug=slug, image=image,
                                             description=description, price=price, available=available, created=created,
                                             uploaded=uploaded, id_in_warehouse=id_in_warehouse)
                new.genre.add(Genre.objects.get(id=item['genre']))



    # warehouse = "http://127.0.0.1:8001/book/"
    # json_result = requests.get(warehouse).json()
    # pk = data.get("pk")
    #
    # for book in json_result:
    #     if not Product.objects.filter(pk=pk).exists():
    #         Product.objects.create(
    #             id_in_warehouse=pk,
    #         )

    # if quote_counter == 5:
    #     send_mail(
    #         "Success!",
    #         "5 new quotes are successfully added!",
    #         settings.NOREPLY_EMAIL,
    #         ["test@noreply.com"],
    #         fail_silently=False,
    #     )
    #     break

