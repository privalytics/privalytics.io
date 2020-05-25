from django.urls import path

from tracker.views import WebsiteStats, ReferrersView, ReferrerDetails, PageDetails

urlpatterns = [
    path('ws/<str:website_url>', WebsiteStats.as_view(), name='website'),
    path('ws/<str:website_url>/referrers', ReferrersView.as_view(), name='referrers'),
    path('ws/<str:website_url>/referrers/<str:ref_name>', ReferrerDetails.as_view(), name='referrer-details'),
    path('ws/<str:website_url>/pages/<path:page_name>', PageDetails.as_view(), name='page-details'),
]