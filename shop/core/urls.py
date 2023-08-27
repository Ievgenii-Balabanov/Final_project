from django.contrib import admin
from django.urls import path, include


from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include("Cart.urls", namespace='cart')),
    path("", include("shop.urls")),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/profile/", views.UserProfile.as_view(), name="profile"),
    # path("accounts/update_profile/", views.UpdateProfileView.as_view(), name="update_profile"),
]
