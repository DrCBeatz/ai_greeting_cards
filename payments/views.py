# payments/views.py

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

PRICE_PER_CREDIT = 0.50 # $0.50 for 10 credits

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        credits = int(request.POST.get("credits", 10)) # Default to 10 credits
        price_in_cents = int(PRICE_PER_CREDIT * credits * 10)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "cad",
                        "unit_amount": price_in_cents,
                        "product_data": {
                            "name": f"{credits} Credits",
                            "description": "Credits for AI Greeting Cards App",
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