from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"book", views.BookViewSet, basename="book")
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"genre", views.GenreViewSet, basename="genre")

urlpatterns = [
    path("", include(router.urls)),
    path("json_dumpdata", views.dumpdata_api_view),
    path("create_order/", views.create_order),
]
