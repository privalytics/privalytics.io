"""
    process_raw_tracks
    ------------------
    This script is used to continuously process RAW tracks. It is an infinite loop, that should be triggered from within
    a supervisor instance. In case there is a big build up of tracks (i.e. the website is accumulating more than what
    it can process, it will warn the admins.)

    It can be used like this::

        $ ./manage.py process_raw_tracks

    It will start an infinite loop and therefore it won't stop unless interrupted.
"""
import time

from django.core.mail import mail_admins
from django.core.management import BaseCommand

from accounts.models import Profile
from tracker.models import RawTracker, Tracker, Website
from urllib.parse import urlparse
from django.http import QueryDict
from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2
import logging

from util.normalize_referrers import normalize_referrer
from util.normalize_websites import normalize_website

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Checkes the raw logs and generates final trackers based on them
    """

    def handle(self, *args, **options):
        logger.info('Starting the processing of raw tracks')
        t0 = time.time()
        total_raw_trackers_analysed = 0
        admins_warned = False
        running_time = 0
        while True:
            t1 = time.time()
            raw_trackers = RawTracker.objects.filter(processed=False)
            total_raw_trackers_analysed += raw_trackers.count()
            for raw_tracker in raw_trackers:
                # Let's verify account:
                try:
                    profile = Profile.objects.get(account_id=raw_tracker.account_id)
                except Profile.DoesNotExist:
                    raw_tracker.ip = None
                    raw_tracker.wrong_account_id = True
                    raw_tracker.processed = True
                    raw_tracker.save()
                    continue
                parsed_url = urlparse(raw_tracker.url)
                queries = QueryDict(parsed_url.query, mutable=False)
                website_url = normalize_website(parsed_url.hostname)
                page = parsed_url.path
                if not page:
                    page = '/'

                utm_source = queries.get('utm_source')
                try:
                    website = Website.objects.get(website_url=website_url)
                except Website.DoesNotExist:
                    raw_tracker.ip = None
                    raw_tracker.website_does_not_exist = True
                    raw_tracker.processed = True
                    raw_tracker.save()
                    continue

                if website.owner != profile.user:
                    raw_tracker.ip = None
                    raw_tracker.wrong_owner = True
                    raw_tracker.processed = True
                    raw_tracker.save()

                referrer_url = None
                referrer_page = '/'
                if raw_tracker.referrer:
                    parsed_referrer = urlparse(raw_tracker.referrer)
                    referrer_url = normalize_referrer(normalize_website(parsed_referrer.hostname))
                    if 'google' in referrer_url:
                        referrer_url = 'google'
                    if 'bing' in referrer_url:
                        referrer_url = 'bing'
                    referrer_page = parsed_referrer.path

                tracker = Tracker.objects.create(
                    url=website_url,
                    page=page,
                    website=website,
                    referrer_url=referrer_url,
                    referrer_page=referrer_page,
                    timestamp=raw_tracker.timestamp,
                    utm_source=utm_source,
                    raw_tracker=raw_tracker,
                )

                if not raw_tracker.dnt:
                    user_agent = parse(raw_tracker.user_agent)
                    operating_system = user_agent.os.family
                    device_family = user_agent.device.family
                    browser = user_agent.browser.family

                    if user_agent.is_mobile:
                        type_device = Tracker.MOBILE
                    elif user_agent.is_tablet:
                        type_device = Tracker.TABLET
                    elif user_agent.is_pc:
                        type_device = Tracker.PC
                    elif user_agent.is_bot:
                        type_device = Tracker.BOT
                    else:
                        type_device = Tracker.UNKNOWN

                    tracker.screen_height = raw_tracker.screen_height
                    tracker.screen_width = raw_tracker.screen_width

                    tracker.operating_system = operating_system
                    tracker.device_family = device_family
                    tracker.browser = browser
                    tracker.type_device = type_device

                    tracker.save()

                    if profile.can_geolocation and not user_agent.is_bot:
                        if raw_tracker.ip:
                            geo = GeoIP2()
                            try:
                                location_data = geo.city(raw_tracker.ip)
                                tracker.country = location_data.get('country_code', '') or ''
                                tracker.region = location_data.get('region', '') or ''
                            except:
                                pass
                    raw_tracker.ip = None

                    tracker.save()
                raw_tracker.processed = True
                raw_tracker.save()

            t2 = time.time()
            running_time += t2-t1
            # When it finishes one loop, check for the already available Raw Trackers
            # If there are already more than when it started, it is a problem, we are lagging behind

            new_raw_trackers = RawTracker.objects.filter(processed=False).count()

            if new_raw_trackers > raw_trackers.count():
                logger.warning("The raw tracker is lagging behind")
                if not admins_warned:
                    message = """ Dear admin,
                    The raw tracker process task has just analysed {} Raw Tracks in {} seconds but there are already
                    {} new tracks to analyse. The taks is running behind and something has to be done.
                    """.format(raw_trackers.count(), t2-t1, new_raw_trackers)
                    subject = "[WARNING] Raw tracks processing lagging behind"
                    try:
                        mail_admins(subject, message, fail_silently=False)
                        admins_warned = True
                    except:
                        logger.error('Failed sending warning e-mail to admins')

            if t2-t0 > 12*60*60:  # Log the statistics every 12 hours
                logger.info('Processed {} tracks in {}s at a rate of {}tracks/s'\
                        .format(total_raw_trackers_analysed, running_time, total_raw_trackers_analysed/running_time))
                running_time = 0
                total_raw_trackers_analysed = 0
                t0 = time.time()

            time.sleep(60*30)  # It sleeps for 30 minutes before going to new batch

