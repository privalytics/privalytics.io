import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from subscriptions.models import SubscriptionType, StripeCustomer, StripePaymentIntent

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddSubscription(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/new_subscription.html'


class NewSubscription(View):
    template_name = 'subscriptions/checkout.html'

    def get(self, request, subscription_slug):
        subscription = get_object_or_404(SubscriptionType, slug=subscription_slug)

        try:
            stripe_customer = StripeCustomer.objects.get(user=self.request.user)
        except StripeCustomer.DoesNotExist:
            customer = stripe.Customer.create(description='Created while checking out Privalytics',
                            email=self.request.user.email)
            stripe_customer = StripeCustomer.objects.create(user=self.request.user, stripe_id=customer.id)

        payment_intent = stripe.PaymentIntent.create(
            amount=subscription.yearly_price*100,
            currency='usd',
            payment_method_types=['card'],
            customer=stripe_customer.stripe_id,
            metadata={'subscription': subscription.slug
            }
        )

        StripePaymentIntent.objects.create(
            user=request.user,
            stripe_customer_id=stripe_customer.stripe_id,
            payment_intent_id=payment_intent.id,
            amount=subscription.yearly_price*100,
            currency='usd',
            subscription=subscription,
        )

        ctx = {
            'subscription': subscription,
            'client_secret': payment_intent.client_secret,
            'stripe_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, self.template_name, ctx)


class SuccessOrCancel(View):
    def get(self, request):
        print(request.GET)
        return HttpResponse({'message': 'OK'})

    def post(self, request):
        print(request.POST)
        return HttpResponse({'message': 'OK'})
