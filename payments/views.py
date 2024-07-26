# payments/views.py

import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import HttpResponse

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

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)
        
        if event["type"] == "checkout.session.completed":
            print("Payment successful")
        
        return HttpResponse(status=200)
