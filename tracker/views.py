from datetime import timedelta, datetime

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now, make_aware
from django.views import View

from tracker.forms import DateRangeForm
from tracker.models import Website


class WebsiteStats(View):
    template_name = 'tracker/website_stats.html'

    def get_context(self, website, start_date, end_date):
        visitors = website.get_daily_visits(start_date, end_date)
        total_views = website.get_page_views(start_date, end_date)
        total_visitors = website.get_uniques(start_date, end_date)
        referrers = website.get_top_referrers(start_date, end_date)
        pages = website.get_top_pages(start_date, end_date)
        devices = website.get_top_devices(start_date, end_date)
        operating_systems = website.get_top_os(start_date, end_date)
        screen_widths = website.get_top_screen_width(start_date, end_date)
        screen_width = website.get_screen_width(start_date, end_date)

        xl = screen_width.filter(screen_width__gte=1200).count()
        lg = screen_width.filter(screen_width__gte=992, screen_width__lt=1200).count()
        md = screen_width.filter(screen_width__gte=768, screen_width__lt=992).count()
        sm = screen_width.filter(screen_width__gte=576, screen_width__lt=768).count()
        xs = screen_width.filter(screen_width__lt=576).count()
        screens = {
            'xl': xl,
            'lg': lg,
            'md': md,
            'sm': sm,
            'xs': xs
        }
        # Need to do this to preserve templates
        referrers = [{
            'referrer_url': referrers['referrers_list'][i],
            'visits': referrers['visits'][i]
        } for i in range(len(referrers['referrers_list']))]

        visit_lengths = []

        for page in pages:
            lengths = website.get_session_length(start_date, end_date, page['page'])
            visit_lengths.append({
                'page': page,
                'length': lengths,
            })

        ctx = {}
        ctx.update({
            'visitors': visitors,
            'total_views': total_views,
            'total_visitors': total_visitors,
            'referrers': referrers,
            'pages': visit_lengths,
            'devices': devices,
            'operating_systems': operating_systems,
            'screen_widths': screen_widths,
            'screens': screens,

        })
        ctx.update({'website': website})

        if website.owner.profile.can_geolocation:
            countries = website.get_top_countries(start_date, end_date)
            ctx.update({'countries': countries})
        return ctx

    def get(self, request, website_url):
        start_date = now()-timedelta(days=30)
        end_date = now()

        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')

        ctx = self.get_context(website, start_date, end_date)
        ctx.update({'form': DateRangeForm(initial={'date_range': (start_date, end_date)})})
        return render(request, self.template_name, ctx)

    def post(self, request, website_url):
        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date_range'][0]
            end_date = form.cleaned_data['date_range'][1]
            ctx = self.get_context(website, start_date, end_date)
            ctx.update({'form': form})
            return render(request, self.template_name, ctx)
        return redirect(website.get_absolute_url())


class ReferrersView(View):
    template_name = 'tracker/referrer_stats.html'

    def get_context(self, website, start_date, end_date):
        # Get top 10 referrers
        referrers = website.get_top_referrers(start_date, end_date)
        # Get top landing page
        landing_page = website.get_top_landing_pages(start_date, end_date, 1)

        ctx = {
            'referrers': referrers,
            'landing_page': landing_page,
        }

        refs = [{
            'referrer_url': referrers['referrers_list'][i],
            'visits': referrers['visits'][i]
        } for i in range(len(referrers['referrers_list']))]
        ctx.update({'refs': refs})
        ctx.update({'website': website})
        return ctx

    def get(self, request, website_url):
        start_date = now() - timedelta(days=30)
        end_date = now()

        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')

        ctx = self.get_context(website, start_date, end_date)
        ctx.update({'form': DateRangeForm(initial={'date_range': (start_date, end_date)})})

        return render(request, self.template_name, ctx)

    def post(self, request, website_url):
        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date_range'][0]
            end_date = form.cleaned_data['date_range'][1]
            ctx = self.get_context(website, start_date, end_date)
            ctx.update({'form': form})
            return render(request, self.template_name, ctx)
        return redirect(website.get_absolute_url())


class PageDetails(View):
    template_name = 'tracker/page_details.html'

    def get_context(self, website, start_date, end_date, page_name):
        page_name = '/' + page_name + '/'
        ctx = {}

        visits = website.get_views_page(page_name, start_date, end_date)
        referrers = website.get_referrers_page(page_name, start_date, end_date)
        internal_links = website.get_internal_links(page_name, start_date, end_date)

        ctx.update({
            'visits': visits,
            'referrers': referrers['referrers_list'],
            'referrer_vistis': referrers['visits'],
            'internal_links': internal_links,
            # 'internal_visits': internal_links['visits_list'],
            'landing_pages': [],
        })

        ctx.update({'website': website})
        ctx.update({'ref_name': page_name})

        return ctx

    def get(self, request, website_url, page_name):
        start_date = now() - timedelta(days=30)
        end_date = now()
        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')

        ctx = self.get_context(website, start_date, end_date, page_name)
        ctx.update({'form': DateRangeForm(initial={'date_range': (start_date, end_date)})})

        return render(request, self.template_name, ctx)

class ReferrerDetails(View):
    template_name = 'tracker/referrer_details.html'

    def get_context(self, website, start_date, end_date, ref_name):
        ctx = {}

        visits = website.get_visits_referrer(start_date, end_date, ref_name)
        pages = website.get_top_referrer_pages(start_date, end_date, ref_name)
        landing_pages = website.get_top_pages_referrer(start_date, end_date, ref_name)

        ctx.update({
            'visits': visits,
            'pages': pages,
            'landing_pages': landing_pages
        })

        ctx.update({'website': website})
        ctx.update({'ref_name': ref_name})
        return ctx

    def get(self, request, website_url, ref_name):
        start_date = now() - timedelta(days=30)
        end_date = now()
        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')

        ctx = self.get_context(website, start_date, end_date, ref_name)
        ctx.update({'form': DateRangeForm(initial={'date_range': (start_date, end_date)})})
        return render(request, self.template_name, ctx)

    def post(self, request, website_url, ref_name):
        website = get_object_or_404(Website, website_url=website_url)
        if not website.is_public and not self.request.user.has_perm('can_view_website', website):
            return redirect('login')
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date_range'][0]
            end_date = form.cleaned_data['date_range'][1]
            ctx = self.get_context(website, start_date, end_date, ref_name)
            ctx.update({'form': form})
            return render(request, self.template_name, ctx)
        return redirect(website.get_absolute_url())
