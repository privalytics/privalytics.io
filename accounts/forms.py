from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import WaitingList
from tracker.models import Website
from util.normalize_websites import normalize_website


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MyUserCreationForm, self).__init__(*args, **kwargs)


class MyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MyModelForm, self).__init__(*args, **kwargs)


class SignUpForm(MyUserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    label_suffix = ''

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this e-mail already exists")
        return email


class WaitingListForm(MyModelForm):
    class Meta:
        model = WaitingList
        fields = ('name', 'email', 'website')

class WebsiteCreationForm(MyModelForm):

    def clean_website_url(self):
        website_url = self.cleaned_data['website_url']
        website_url = normalize_website(website_url)
        if Website.objects.filter(website_url=website_url).exists():
            raise forms.ValidationError("This website was already registered")
        return website_url

    class Meta:
        model = Website
        fields = ('website_url', 'website_name')


class ContactInformation(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        if 'email' in self.changed_data:
            self.instance.profile.email_validated = False
            self.instance.profile.save()
        user = super(ContactInformation, self).save(commit)
        user.profile.send_activation_email()
        return user
