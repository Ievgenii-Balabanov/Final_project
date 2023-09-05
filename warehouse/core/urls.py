from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", ObtainAuthToken.as_view()),
    path("", include("warehouse.urls")),
]
