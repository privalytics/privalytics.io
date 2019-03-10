from django.contrib import admin

from subscriptions.models import SubscriptionType, StripeCustomer, StripePaymentIntent

admin.site.register((
    SubscriptionType,
    StripeCustomer,
    StripePaymentIntent
))
