from django.urls import path
from django.views.generic import TemplateView

from backend.views import ContactView, SupportView

urlpatterns = [
    path('contact', ContactView.as_view(), name='contact'),
    path('contact-success', TemplateView.as_view(template_name='backend/contact-success.html'), name='contact-success'),
    path('support', SupportView.as_view(), name='support'),
    path('support-success', TemplateView.as_view(template_name='backend/support-success.html'), name='support-success'),
]