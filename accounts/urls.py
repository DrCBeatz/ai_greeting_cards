# accounts/urls.py

from django.urls import path
from .views import user_login, SignupPageView, add_credits

urlpatterns = [
    path('login/', user_login, name='login'),
    path("signup/", SignupPageView.as_view(), name="signup"),
    path('add-credits/<int:amount>/', add_credits, name='add_credits'),
]
