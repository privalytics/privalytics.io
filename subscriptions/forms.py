from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(max_length=255, help_text='Your complete name')
    email = forms.EmailField()
    address = forms.CharField