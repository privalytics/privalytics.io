from django.urls import path

from api.views import TrackerView, BeatView

urlpatterns = [
    path('tracker', TrackerView.as_view(), name='tracker-api'),
    path('beat', BeatView.as_view(), name='beat-api'),
]
