from django.core.management import BaseCommand

from tracker.models import Tracker


class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        trackers = Tracker.objects.filter(page=None)

        for tr in trackers:
            tr.page = '/'
            tr.save()

        trackers = Tracker.objects.filter(page='')

        for tr in trackers:
            tr.page = '/'
            tr.save()
