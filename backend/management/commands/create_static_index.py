import os

from django.core.management import BaseCommand
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = """Creates a static index file
    """

    def handle(self, *args, **options):
        if not os.path.exists('static_pages'):
            os.makedirs('static_pages')
        if not os.path.exists('static_pages/privacy'):
            os.makedirs('static_pages/privacy')
        if not os.path.exists('static_pages/terms'):
            os.makedirs('static_pages/terms')
        if not os.path.exists('static_pages/data-collection'):
            os.makedirs('static_pages/data-collection')

        txt = render_to_string('privalytics/index.html')
        with open('static_pages/index.html', 'w') as f:
            f.write(txt)

        txt = render_to_string('privalytics/privacy.html')
        with open('static_pages/privacy/index.html') as f:
            f.write(txt)

        txt = render_to_string('privalytics/terms.html')
        with open('static_pages/terms/index.html') as f:
            f.write(txt)

        txt = render_to_string('privalytics/data_collection.html')
        with open('static_pages/data-collection') as f:
            f.write(txt)
