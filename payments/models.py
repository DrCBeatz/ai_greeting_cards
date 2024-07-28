# payments/models.py

from django.db import models
from django.conf import settings

class Payment(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('complete', 'Complete'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='CAD')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    cardholder_email = models.EmailField(blank=True, null=True)
    cardholder_name = models.CharField(max_length=255, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} {self.currency} by {self.user.username}"
