from django.contrib import admin

from backend.models import Message, SupportMessage

admin.site.register((
    Message,
    SupportMessage
))
