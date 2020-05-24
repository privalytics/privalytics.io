from django.contrib import admin

from accounts.models import Profile, Subscription, WaitingList

admin.site.register((
    Profile,
    Subscription,
    WaitingList,
))