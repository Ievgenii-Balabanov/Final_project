from django.db import models

STATUS = (
    (0, "cart"),
    (1, "ordered"),
    (2, "success"),
    (3, "fail"),
)


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField()
    quantity = models.IntegerField()
    id_in_store = models.IntegerField()


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    delivery_address = models.CharField(max_length=140)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Book, unique=False, on_delete=models.PROTECT)
    ordered = models.BooleanField(default=False)
