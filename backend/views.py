from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from backend.models import Message, SupportMessage


class ContactView(CreateView):
    model = Message
    fields = ('user_email', 'message')
    template_name = 'backend/contact.html'
    success_url = reverse_lazy('contact-success')


class SupportView(LoginRequiredMixin, CreateView):
    model = SupportMessage
    fields = ('message', )
    template_name = 'backend/support.html'
    success_url = reverse_lazy('support-success')

    def form_valid(self, form):
        support_message = form.save(commit=False)
        support_message.user = self.request.user
        support_message.save()
        return super(SupportView, self).form_valid(form)
