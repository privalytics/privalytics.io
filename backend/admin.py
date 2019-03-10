from django.contrib import admin

from backend.models import Message, SupportMessage, AccountTypes, AsyncEmail

admin.site.register((
    Message,
    SupportMessage,
    AccountTypes,
    AsyncEmail,

))
