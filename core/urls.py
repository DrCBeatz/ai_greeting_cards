# core/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts.views import custom_logout_view, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aigreetingcards.urls')),
    path('accounts/login/', user_login, name='login'),
    path("accounts/logout/", custom_logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
]
