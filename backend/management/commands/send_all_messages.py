import logging
from time import time

from django.core.management import BaseCommand

from backend.models import AsyncEmail

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        t0 = time()
        messages = AsyncEmail.objects.filter(sent=False)
        logger.info('Going to send {} emails'.format(messages.count()))
        for message in messages:
            message.send()
        logger.info('Sent all messages in {} seconds'.format(time()-t0))
