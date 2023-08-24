from django.db import models

PLACE = (
    (0, "in_the_warehouse"),
    (1, "on_the_shelf"),
)

STATUS = (
    (0, "in_work"),
    (1, "success"),
    (2, "fail"),
)


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField()


class BookItem(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    place = models.IntegerField(choices=PLACE, default=0)


class Order(models.Model):
    user_email = models.EmailField()
    status = models.IntegerField(choices=STATUS, default=0)
    delivery_address = models.CharField(max_length=200)
    order_id_in_shop = models.IntegerField()


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    warehouse_book_id = models.ForeignKey(Book, on_delete=models.CASCADE)


class BookItemOrderItem(models.Model):
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    book_item_id = models.ForeignKey(BookItem, on_delete=models.CASCADE)
