from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import now

from accounts.tokens import account_activation_token
from subscriptions.models import SubscriptionType, Subscription


class Profile(models.Model):
    """ Class to extend the user model. It will be useful at some point.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    email_validated = models.BooleanField(default=False)
    email_validated_date = models.DateTimeField(auto_now_add=False, null=True)
    account_id = models.CharField(max_length=12, unique=True)
    max_websites = models.IntegerField(default=1, help_text='maximum number of websites that you can register')
    can_geolocation = models.BooleanField(default=False, null=True)
    monthly_views = models.IntegerField(default=0, help_text='number of views registered in the last month')
    maximum_views = models.IntegerField(default=0, help_text='maximum number of views across all websites')
    account_selected_signup = models.CharField(null=True, blank=True, max_length=50, help_text='The account type '
                                                                                   'selected while signing up')

    @property
    def account_type(self):
        subscription = Subscription.objects\
            .filter(user=self.user, expiration_date__gte=now())\
            .order_by('-expiration_date')
        if subscription.count():
            return subscription.first().subscription_type.name
        else:
            return "No active subscription"

    def __str__(self):
        return "Profile(email={})".format(self.user.email)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_id = "PL-" + uuid.uuid4().hex[:6].upper()
        super(Profile, self).save(*args, **kwargs)

    def send_activation_email(self, current_site=None):
        current_site = current_site or settings.WEBSITE_URL
        subject = 'Activate Your Privalytics Account'
        message = render_to_string('emails/account_activation.txt', {
            'user': self.user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)).decode('utf-8'),
            'token': account_activation_token.make_token(self.user),
        })
        self.user.email_user(subject, message, from_email='Privalytics <noreply@privalytics.io>')


class WaitingList(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(blank=False, null=False, unique=True)
    website = models.CharField(max_length=255, blank=False)
    account_type = models.CharField(max_length=50, null=True, blank=True)
    sign_up_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return f"{self.name} <{self.email}>"
        return f"self.email"



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
