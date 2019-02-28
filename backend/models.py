import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils.timezone import now


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


class AccountTypes(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    max_websites = models.IntegerField(default=0, null=False, blank=False)
    max_visits = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return "Account Type {}".format(self.name)


class AsyncEmail(models.Model):
    """ Model to store information about messages to send. This allows to send e-mails asynchronously at given intervals
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    sent_time = models.DateTimeField(auto_now_add=False, null=True)
    sent = models.BooleanField(default=False)
    to_name = models.CharField(max_length=255, null=False, blank=False)
    to_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=255)
    msg_txt = models.TextField()
    from_name = models.CharField(max_length=255, null=True, blank=True)
    from_email = models.EmailField(null=True, blank=True)

    def send(self):
        if not self.from_name:
            self.from_name = settings.DEFAULT_FROM_NAME
        if not self.from_email:
            self.from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(
                self.subject,
                self.msg_txt,
                '{} <{}>'.format(self.from_name, self.from_email),
                ['{} <{}>'.format(self.to_name, self.to_email)],
                fail_silently=False,
            )
            self.sent = True
            self.sent_time = now()
            self.save()
        except Exception as e:
            logger.error("Problem sending email to {}".format(self.to_email))
            logger.exception(e)

    def __str__(self):
        if self.sent:
            return "Email sent to {}<{}>".format(self.to_name, self.to_email)
        return "Email to send to {}<{}>".format(self.to_name, self.to_email)
