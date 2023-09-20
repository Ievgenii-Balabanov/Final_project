from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path("", views.index, name="index"),

    path("registration/", views.RegisterFormView.as_view(), name="register"),
    path("login/", views.LoginFormView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("book/", views.BookListView.as_view(), name="book-list"),
    path("latest_book/", views.LatestBookListView.as_view(), name="latest-book-list"),
    # path("latest_book/", views.latest_book, name="latest-book-list"),
    path("book/<int:pk>/<slug:slug>/", views.BookInstanceDetailView.as_view(), name="book-detail"),
    path("filter/", views.FilterBookByGenre.as_view(), name="genre-filter"),

    path("create/", views.order_create, name='order-create'),
    path("contact/", views.contact, name="contact"),
]
