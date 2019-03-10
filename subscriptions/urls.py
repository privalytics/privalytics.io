from django.urls import path

from subscriptions.api import ValidateSubscription
from subscriptions.views import AddSubscription, SuccessOrCancel, NewSubscription

urlpatterns = [
    path('new', AddSubscription.as_view(), name='subscriptions'),
    path('new/<subscription_slug>', NewSubscription.as_view(), name='new-subscription'),
    path('validate', ValidateSubscription.as_view(), name='validate'),
    path('success', SuccessOrCancel.as_view(), name='success'),
    path('cancel', SuccessOrCancel.as_view(), name='cancel'),
]
