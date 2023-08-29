from django.urls import path, include
from . import views

app_name = "Cart"


urlpatterns = [
    path("", views.cart_detail, name='cart_detail'),
    path("add/<int:pk>", views.cart_add, name='cart_add'),
    path("remove/<int:pk>/", views.cart_remove, name='cart_remove'),
]

