# payments/admin.py

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'created_at')
    search_fields = ('user__username', 'stripe_payment_intent_id', 'stripe_checkout_session_id')
    list_filter = ('currency', 'created_at')
