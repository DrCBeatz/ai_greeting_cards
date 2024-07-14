# accounts/urls.py

from django.urls import path
from .views import user_login, custom_logout_view, SignupPageView

urlpatterns = [
    path('login/', user_login, name='login'),
    path("logout/", custom_logout_view, name="logout"),
    path("signup/", SignupPageView.as_view(), name="signup"),
]
