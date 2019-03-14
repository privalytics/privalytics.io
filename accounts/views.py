from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import login as auth_login
from accounts.forms import SignUpForm, WebsiteCreationForm, ContactInformation
from accounts.models import Subscription
from accounts.tokens import account_activation_token
from tracker.models import Website


class SignUpView(View):
    template_name = 'accounts/sign_up.html'

    def get(self, request, account_type=None):
        form = SignUpForm()
        request.session['account_type'] = account_type
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.account_selected_signup = request.session.get('account_type')
            user.save()
            user.profile.save()
            user.profile.send_activation_email(current_site=get_current_site(request).domain)
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_validated = True
            user.profile.email_validated_date = now()
            user.save()
            auth_login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
        else:
            return render(self.request, 'accounts/activation_failed.html')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        ctx = {}
        websites = request.user.websites.all()
        account_id = request.user.profile.account_id
        ctx.update({'websites': websites, 'account_id': account_id})
        return render(request, 'accounts/dashboard.html', ctx)


class CreateWebsite(LoginRequiredMixin, CreateView):
    model = Website
    form_class = WebsiteCreationForm
    template_name = 'accounts/new_website.html'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            total_websites = request.user.websites.count()
            if request.user.profile.max_websites:
                if total_websites >= request.user.profile.max_websites:
                    form.errors[NON_FIELD_ERRORS] = ['You can\'t register more websites']
                    return render(request, self.template_name, {'form': form})
            website = form.save(commit=False)
            website.owner = request.user
            website.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


class AccountView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account.html'
    model = User
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super(AccountView, self).get_context_data(**kwargs)
        account_type = self.request.user.profile.account_type
        website_count = self.request.user.websites.count()
        website_total = self.request.user.profile.max_websites
        views_count = self.request.user.profile.monthly_views
        views_total = self.request.user.profile.maximum_views
        geoip_active = self.request.user.profile.can_geolocation

        ctx.update({
            'account_type': account_type,
            'website_count': website_count,
            'website_total': website_total,
            'views_count': views_count,
            'views_total': views_total,
            'geoip_active': geoip_active
        })
        return ctx


class SubscriptionView(LoginRequiredMixin, View):
    template_name = 'accounts/subscription.html'

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=self.request.user)
        ctx = {
            'subscriptions': subscriptions
        }
        return render(request, self.template_name, ctx)

