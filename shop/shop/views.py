from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from Cart.cart import Cart
from .forms import RegisterForm, ParForm, OrderCreateForm
from .models import Category, Product, OrderItem


# from shop.forms import CartAddProductForm
# from .utils import cartData


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


class BookListView(generic.ListView):
    model = Product
    template_name = "shop/book_list.html"
    paginate_by = 5
    queryset = Product.objects.all()


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


def checkout(request):
    # data = cartData(request)

    # cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']

    # context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/checkout.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def order_create(request):
    cart = Cart(request)
    if request.POST:
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         book=item["product"],
                                         price=item['price'],
                                         quantity=item['quantity'])
                cart.clear()
                return render(request, 'shop/orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'shop/orders/order/create.html',
                  {'cart': cart, 'form': form})
