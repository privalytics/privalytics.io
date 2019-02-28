from django.core.management import BaseCommand

from tracker.models import Tracker


class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        trackers = Tracker.objects.exclude(referrer_url=None)\
            .filter(referrer_page=None)

        for tr in trackers:
            tr.referrer_page = '/'
            tr.save()

        trackers = Tracker.objects.exclude(referrer_url=None)\
            .filter(referrer_page='')

        for tr in trackers:
            tr.referrer_page = '/'
            tr.save()
