import requests
import json
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView

from Cart.cart import Cart
from .forms import ParForm, RegisterForm
from .models import Category, Genre, Order, OrderItem, Product
from shop.tasks import add_order_to_warehouse


def index(request):
    return render(request, "index.html")


class RegisterFormView(generic.FormView):
    template_name = "registration/registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy("shop:index")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user = form.save()

        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('shop:index')


def logout_view(request):
    logout(request)
    return redirect('shop:index')


class BookGenre:
    """
    Book genres
    """

    def get_genres(self):
        return Genre.objects.all()


class BookListView(BookGenre, generic.ListView):
    model = Product
    template_name = "shop/book_list.html"
    queryset = Product.objects.all()  # -> Product is a shop model
    paginate_by = 8


class BookInstanceDetailView(generic.DetailView):
    model = Product
    template_name = "shop/book_detail.html"
    context_object_name = "book"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        obj = queryset.get()
        return obj

    def get_success_url(self):
        return reverse_lazy("shop:book-detail", kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part_form'] = ParForm()  # Your part form
        return context


def order_create(request):
    cart = Cart(request)
    if request.POST:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        delivery_address = request.POST.get("delivery_address")
        postal_code = request.POST.get("postal_code")
        city = request.POST.get("city")
        order = Order.objects.create(first_name=first_name, last_name=last_name, email=email,
                                     delivery_address=delivery_address, postal_code=postal_code, city=city)
        order.save()

        for item in cart:
            order_item = OrderItem.objects.create(order=order, book=item["product"], price=item['price'],
                                                  quantity=item['quantity'])

            add_order_to_warehouse.apply_async(args=[order.pk])
            print(order.pk)
            cart.clear()
            return render(request, 'shop/orders/order/created.html',
                          {'order': order})

    else:
        return render(request, "shop/orders/order/create.html", {'cart': cart})
    return render(request, "shop/orders/order/create.html", {'cart': cart, 'order': order})


class FilterBookByGenre(BookGenre, ListView):
    """
    Books filtering by genre
    """

    template_name = "shop/genre_list.html"

    def get_queryset(self):
        queryset = Product.objects.filter(genre__in=self.request.GET.getlist("genre"))
        return queryset


def warehouse_new_order(request):
    orders = Order.objects.all().values("id", "first_name", "last_name", "email", "delivery_address", "postal_code",
                                        "city", "created_on", "updated_on", "payment")
    order_items = OrderItem.objects.all().values("id", "order", "book", "price", "quantity")

    order_list = list(orders)
    order_items_list = list(order_items)
    return JsonResponse([order_list, order_items_list], safe=False)
