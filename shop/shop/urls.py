from django.urls import path
from . import views

app_name = 'shop'

# urlpatterns = [
#     path("", views.index, name="index"),
#     # path("book/", views.BookListView.as_view(), name="book-list"),
#     path("registration/", views.RegisterFormView.as_view(), name="register"),
#     path("login/", views.LoginFormView.as_view(), name="login"),
#     # path("book/", views.BookListView.as_view(), name="book-list"),
#     # path("book/<int:pk>", views.BookInstanceDetailView.as_view(), name="book-detail"),
#     # path("cart/", views.cart, name="cart"),
#     path('checkout/', views.checkout, name="checkout"),
#     path('<slug:category_slug>/', views.product_list,
#          name='product_list_by_category'
#          ),
#     path('<int:id>/<slug:slug>', views.product_detail,
#          name='product_detail')
# ]


urlpatterns = [
    path("", views.product_list, name='product_list'),
    path('^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    path('<int:id>/<slug:slug>',
        views.product_detail,
        name='product_detail'),
]
