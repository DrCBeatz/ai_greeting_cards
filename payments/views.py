# products/views.py

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

PRICE = 5 # $5 for 20 Images or 200 Credits

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "cad",
                        "unit_amount": int(PRICE) * 100,
                        "product_data": {
                            "name": "Credits",
                            "description": "200 Credits for AI Greeting Cards App",
                        },
                    },
                    "quantity": "1",
                }
            ],
            metadata={"product_id": "1"},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
    

class SuccessView(TemplateView):
    template_name = "payments/success.html"

class CancelView(TemplateView):
    template_name = "payments/cancel.html"

class BuyCreditsView(TemplateView):
    template_name = "payments/buy_credits.html"