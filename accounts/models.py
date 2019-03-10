from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token
from backend.models import AccountTypes, AsyncEmail
from subscriptions.models import SubscriptionType


class Profile(models.Model):
    """ Class to extend the user model. It will be useful at some point.
    """
    BEGINNER = 0
    BLOGGER = 1
    ADVANCED = 2
    ACCOUNT_TYPES = (
        (BEGINNER, 'beginner'),
        (BLOGGER, 'blogger'),
        (ADVANCED, 'advanced')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    email_validated = models.BooleanField(default=False)
    email_validated_date = models.DateTimeField(auto_now_add=False, null=True)
    account_id = models.CharField(max_length=12, unique=True)
    account_type = models.IntegerField(choices=ACCOUNT_TYPES, default=BEGINNER, null=False, blank=False)
    max_websites = models.IntegerField(default=0, help_text='maximum number of websites that can be registerd')
    can_geolocation = models.BooleanField(default=False, null=True)
    account_selected = models.CharField(max_length=100, null=True, blank=True)
    monthly_views = models.IntegerField(default=0, help_text='number of views registered in the last month')
    maximum_views = models.IntegerField(default=0, help_text='maximum number of views across all websites')

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
        # user.email_user(subject, message, from_email='Privalytics <noreply@privalytics.io>')
        AsyncEmail.objects.create(
            to_email=self.user.email,
            to_name=self.user.username,
            subject=subject,
            msg_txt=message
        )


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    expiration_date = models.DateTimeField(auto_now_add=False, null=True)
    subscription_date = models.DateTimeField(auto_now_add=True, null=False)
    subscription_type = models.ForeignKey(SubscriptionType, null=False, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
