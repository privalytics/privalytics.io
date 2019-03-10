from datetime import timedelta

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Subscription
from logs.models import MessagesToAdmin
from subscriptions.models import StripePaymentIntent

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentIntentSerializer(serializers.Serializer):
    id = serializers.CharField()


class ValidateSubscription(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        payment_intent = PaymentIntentSerializer(data=request.data.dict())
        if payment_intent.is_valid():
            id = payment_intent.validated_data.get('id')
            pi = stripe.PaymentIntent.retrieve(id)
            try:
                payment_db = StripePaymentIntent.objects.get(payment_intent_id=id)
            except StripePaymentIntent.DoesNotExist:
                MessagesToAdmin.objects.create(message=f"Received a post request for payment intent with id {id}"
                                               f"but it is not registered on the database")
                return Response('')

            if payment_db.amount == pi.amount_received:
                Subscription.objects.create(
                    user=payment_db.user,
                    expiration_date=now()+timedelta(days=365),
                    subscription_type=payment_db.subscription
                )
                payment_db.payed_on = now()
                payment_db.payed = True
                payment_db.save()
                MessagesToAdmin.objects.create(message=f"New subscription {payment_db.subscription} for {payment_db.user} created.")
            else:
                MessagesToAdmin.objects.create(message=f"Payment on DB has a value of {payment_db.amount} while "
                                               f"the payment intent received is of {pi.amount_received}")
        return Response('')
