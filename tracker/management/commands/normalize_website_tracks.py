from django.core.management import BaseCommand

from tracker.models import Tracker
from util.normalize_websites import normalize_website


class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        trackers = Tracker.objects.all()
        for tracker in trackers:
            if tracker.referrer_url:
                tracker.referrer_url = normalize_website(tracker.referrer_url)
            if tracker.url:
                tracker.url = normalize_website(tracker.url)
            tracker.save()
