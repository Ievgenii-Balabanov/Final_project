from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


from shop.forms import RegisterForm
from shop.models import Book, Cart, Order
from shop.utils import cartData


# def index(request):
#     return render(request, "index.html")


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


class BookListView(generic.ListView):
    model = Book
    template_name = "shop/book_list.html"
    paginate_by = 5
    queryset = Book.objects.all()


class BookInstanceDetailView(generic.DetailView):
    model = Book
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


def index(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Book.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'index.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
