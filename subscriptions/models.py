from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class SubscriptionType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(blank=True)
    max_websites = models.IntegerField(default=0, null=False, blank=False)
    max_visits = models.IntegerField(default=0, null=False, blank=False)
    can_geolocation = models.BooleanField(default=False, null=False, blank=False)
    yearly_price = models.IntegerField(default=0, help_text='Yearly price in dollars', null=False, blank=False)
    monthly_price = models.IntegerField(default=0, help_text='Monthly price in dollars', null=False, blank=False)
    stripe_test_id = models.CharField(max_length=50, help_text='Stripe ID for the test account')
    stripe_id = models.CharField(max_length=50, help_text='Stripe ID for the test account')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return f"Subscription Type {self.name}"

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        super(SubscriptionType, self).save(**kwargs)


class StripeCustomer(models.Model):
    """ Store the Stripe Customer ID and associate it with a user on this platform.
    """
    stripe_id = models.CharField(max_length=125, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Stripe ID for {self.user}"


class StripePaymentIntent(models.Model):
    """ Stores the payment intents in order to keep track of who pays what.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=255, null=False)
    payment_intent_id = models.CharField(max_length=255)
    payed = models.BooleanField(default=False)
    payed_on = models.DateTimeField(auto_now_add=False, null=True)
    canceled = models.BooleanField(default=False)
    canceled_on = models.DateTimeField(auto_now_add=False, null=True)
    amount = models.IntegerField(null=False, help_text='Amount in the minimum currency step')
    currency = models.CharField(max_length=10)
    subscription = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True)
