from django.urls import path

from core import settings
from . import views
from .views import logout

app_name = 'shop'

urlpatterns = [
    path("", views.index, name="index"),

    path("registration/", views.RegisterFormView.as_view(), name="register"),
    path("login/", views.LoginFormView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("book/", views.BookListView.as_view(), name="book-list"),
    path("book/<int:pk>/<slug:slug>/", views.BookInstanceDetailView.as_view(), name="book-detail"),
    path("filter/", views.FilterBookByGenre.as_view(), name="genre-filter"),

    path("create/", views.order_create, name='order-create'),
    path("warehouse_new_order/", views.warehouse_new_order, name="warehouse_new_order"),
]
