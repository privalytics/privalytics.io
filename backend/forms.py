from django import forms

from backend.models import Message, SupportMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('user_email', 'message')


class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ('message', )
