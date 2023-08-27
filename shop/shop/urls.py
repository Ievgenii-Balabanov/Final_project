from django.urls import path

from . import views


app_name = "shop"


urlpatterns = [
    path("", views.index, name="index"),
    path("registration/", views.RegisterFormView.as_view(), name="register"),
    path("login/", views.LoginFormView.as_view(), name="login"),
    path("book/", views.BookListView.as_view(), name="book-list"),
    path("book/<int:pk>", views.BookInstanceDetailView.as_view(), name="book-detail"),
    # path("cart/", views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
