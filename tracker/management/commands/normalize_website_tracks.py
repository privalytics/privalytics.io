import logging

from django.core.management import BaseCommand

from tracker.models import Tracker
from util.normalize_websites import normalize_website


logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        trackers = Tracker.objects.exclude(referrer_url=None).exclude(referrer_url='')
        logger.info('Going to normalize {} referrers URLS'.format(trackers.count()))
        for tracker in trackers:
                tracker.referrer_url = normalize_website(tracker.referrer_url)
        trackers = Tracker.objects.exclude(url=None).exclude(url='')
        logger.info('Going to normalize {} trackers URLS'.format(trackers.count()))
        for tracker in trackers:
            if tracker.url:
                tracker.url = normalize_website(tracker.url)
            tracker.save()
