from django.contrib import admin

from accounts.models import Profile, Subscription

admin.site.register((
    Profile,
    Subscription,

))