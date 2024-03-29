from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path("", views.index, name="index"),

    path("registration/", views.RegisterFormView.as_view(), name="register"),
    path("login/", views.LoginFormView.as_view(), name="login"),

    path("book/", views.BookListView.as_view(), name="book-list"),
    path("book/<int:pk>/<slug:slug>", views.BookInstanceDetailView.as_view(), name="book-detail"),

    path("create/", views.order_create, name='order-create'),

]
