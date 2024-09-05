# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('aigreetingcards.urls')),
    path("accounts/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
