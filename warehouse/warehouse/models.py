from django.db import models
from django.urls import reverse


STATUS = (
    (0, "in_work"),
    (1, "success"),
    (2, "fail"),
)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    name = models.CharField(max_length=150, db_index=True)
    genre = models.ManyToManyField(Genre, verbose_name="genre")
    author = models.CharField(max_length=70)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    image = models.ImageField(upload_to="media/", blank=True)
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:book-detail', args=[self.id, self.slug])


class BookItem(models.Model):
    book_id = models.ForeignKey(Book, related_name='books', on_delete=models.CASCADE)


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS)
    shop_order_id = models.IntegerField()

    class Meta:
        ordering = ('created_on',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Client Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class OrderItemBookItem(models.Model):
    order_item_id = models.ForeignKey(OrderItem, related_name='order_items', on_delete=models.CASCADE)
    book_item_id = models.ForeignKey(BookItem, related_name='book_items', on_delete=models.CASCADE)


