# accounts/urls.py

from django.urls import path
from .views import user_login, SignupPageView

urlpatterns = [
    path('login/', user_login, name='login'),
    path("signup/", SignupPageView.as_view(), name="signup"),
]
