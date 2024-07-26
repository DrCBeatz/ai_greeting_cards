# payments/urls.py

from django.urls import path

from .views import (
    BuyCreditsView, 
    CreateStripeCheckoutSessionView, 
    SuccessView, 
    CancelView, 
    StripeWebhookView
    )

urlpatterns = [
    path("buy-credits/", BuyCreditsView.as_view(), name="buy-credits"),
    path(
        "create-checkout-session/",
         CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session",
         ),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]