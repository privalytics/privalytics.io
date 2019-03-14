import logging

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)
class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField(blank=False, help_text='email')
    message = models.TextField(blank=False)

    def __str__(self):
        return "Message from {}".format(self.user_email)


class SupportMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    message = models.TextField(blank=False)
