from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

STATUS = (
    (0, "cart"),
    (1, "ordered"),
    (2, "success"),
    (3, "fail"),
)


# class User(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.EmailField()


class User(AbstractUser):
    email = models.EmailField()


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    quantity = models.IntegerField()
    id_in_store = models.IntegerField()

    def get_absolute_url(self):
        some_id = self.pk
        return reverse("blog:post_detail", kwargs={"pk": some_id})


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    delivery_address = models.CharField(max_length=140)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


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
