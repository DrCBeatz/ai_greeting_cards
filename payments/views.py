import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Payment
from django.template.loader import render_to_string

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

CREDITS_PRICING = {
    100: 500,    # $5.00 in cents
    250: 1200,   # $12.00 in cents
    500: 2250,   # $22.50 in cents
    750: 3250,   # $32.50 in cents
    1000: 4000,  # $40.00 in cents
}

class CreateStripeCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        credits = int(request.POST.get("credits", 100))  # Default to 100 credits
        price_in_cents = CREDITS_PRICING.get(credits)

        if price_in_cents is None:
            # Handle invalid credits value
            return HttpResponse("Invalid number of credits selected.", status=400)

        user_id = request.user.id  # Get the logged-in user's ID

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
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": user_id,
                "credits": credits,
            },
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
            session = event['data']['object']
            user_id = session["metadata"]["user_id"]
            credits_to_add = int(session["metadata"]["credits"])
            user = User.objects.get(id=user_id)

            # Update the user's credits
            user.credits += credits_to_add
            user.save()

            # Extract card details
            payment_intent_id = session.get('payment_intent')
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            payment_method = stripe.PaymentMethod.retrieve(payment_intent.payment_method)

            address = session.get('customer_details', {}).get('address', {})

            # Save payment details
            payment = Payment.objects.create(
                user=user,
                amount=session["amount_total"] / 100,  # Amount in dollars
                currency=session["currency"].upper(),
                stripe_payment_intent_id=payment_intent_id,
                stripe_checkout_session_id=session.get('id'),
                country=address.get('country'),
                postal_code=address.get('postal_code'),
                cardholder_email=payment_method.billing_details.email,
                cardholder_name=payment_method.billing_details.name,
                card_last4=payment_method.card.last4,
                status='complete',
            )

            customer_email = session["customer_details"]["email"]

            email_subject = f"Thank you {user.username} for your purchase!"
            email_message = render_to_string('payments/payment_email.html', {
                'user': user,
                'payment': payment,
                'credits_to_add': credits_to_add,
            })

            send_mail(
                subject=email_subject,
                message=email_message,
                from_email="noreply@aigreetingcards.com",
                recipient_list=[customer_email],
            )
            print("Email sent successfully")

        return HttpResponse(status=200)