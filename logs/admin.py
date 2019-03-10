from django.contrib import admin

from logs.models import TimeToStore, AccountTypeSelected, MessagesToAdmin

admin.site.register((
    TimeToStore,
    AccountTypeSelected,
    MessagesToAdmin,
))
