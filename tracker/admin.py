from django.contrib import admin

from tracker.models import Tracker, Website, RawTracker, BeatTracker

admin.site.register((
    RawTracker,
    BeatTracker,
    Tracker,
    Website,
))
