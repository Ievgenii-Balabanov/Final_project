from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions

from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Warehouse API",
#       default_version='v1',
#       description="Warehouse application",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", ObtainAuthToken.as_view()),
    path("", include("warehouse.urls")),

    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
