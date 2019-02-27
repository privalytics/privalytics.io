from django.contrib import admin

from backend.models import Message, SupportMessage, AccountTypes

admin.site.register((
    Message,
    SupportMessage,
    AccountTypes
))
