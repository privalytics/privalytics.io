from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.forms import WebsiteCreationForm
from tracker.models import Website


class DashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='johnpannel', email='john@pannel.com', password='123')
        user_login = self.client.login(username='johnpannel', password='123')
        self.assertTrue(user_login)

    def test_login_redirects(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTrue(response.status_code, 200)

    def test_dashboard_no_websites(self):
        Website.objects.filter(owner=self.user).delete()
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'You have no websites registered yet')

    def test_create_website_view(self):
        response = self.client.get(reverse('create-website'))
        self.assertEqual(response.status_code, 200)

    def test_create_website_form(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotContains(response, 'Test')
        data = {'website_url': 'www.test.com', 'website_name': 'Test'}
        response = self.client.post(reverse('create-website'), data)
        self.assertRedirects(response, reverse('dashboard'))
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Test')


class DashboardTestFails(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john_failed', email='john_failed@pannel.com', password='123')
        Website.objects.create(website_url='new-test.com', website_name='New Test', owner=user)
        url = reverse('login')
        user_login = self.client.login(username='john_failed', password='123')
        self.assertTrue(user_login)

    def test_create_website_failed(self):
        self.client.login(username='johnpannel2', password='123')
        data = {'website_url': 'www.new-test2.com', 'website_name': 'Test 2'}
        response = self.client.post(reverse('create-website'), data)
        self.assertContains(response, 'register more websites') # Had to trim it because of special characters


class AccountTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john_account', email='john@account.com', password='123')
        user_login = self.client.login(username='john_account', password='123')
        self.assertTrue(user_login)

    def test_account_view(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)

    def test_account_no_active_subscription(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertContains(response, 'No active subscription')