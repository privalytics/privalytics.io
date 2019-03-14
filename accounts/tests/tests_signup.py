from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mailer.engine import send_all

from accounts.forms import SignUpForm
from accounts.models import Profile
from accounts.tokens import account_activation_token


class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_invalid_data(self):
        invalid_data = [
            # Password too short
            {
                'username': 'johanne',
                'email': 'johanne@doe.com',
                'password1': 'ksdhggh',
                'password2': 'ksdhggh'
            },
            # Password too easy
            {
                'username': 'johanne',
                'email': 'johanne@doe.com',
                'password1': '1234abcd',
                'password2': '1234abcd'
            },
            # Email not valid
            {
                'username': 'johanne',
                'email': 'johanne',
                'password1': 'ksdhgghf',
                'password2': 'ksdhgghf'
            },
        ]

        for data in invalid_data:
            form = SignUpForm(data)
            self.failIf(form.is_valid())

    def test_valid_data(self):
        data = {
            'username': 'johanne',
            'email': 'johanne@doe.com',
            'password1': 'ksdhgghf',
            'password2': 'ksdhgghf'
        }
        form = SignUpForm(data)
        self.failUnless(form.is_valid())
        form.save()
        self.assertTrue(User.objects.filter(email='johanne@doe.com').exists())

    def test_unique_email(self):
        data = {
            'username': 'johanne',
            'email': 'john@doe.com',
            'password1': 'ksdhgghf',
            'password2': 'ksdhgghf'
        }

        form = SignUpForm(data)
        self.failIf(form.is_valid())

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_sign_up_response_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_profile_exists(self):
        self.assertTrue(Profile.objects.exists())


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
            'email': 'joh@doe.com'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('index')
        self.account_url = reverse('dashboard')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the account page
        '''
        self.assertRedirects(self.response, self.account_url)

    def test_email_sent(self):
        send_all()  # Django-mailer to send all messages
        self.assertGreater(len(mail.outbox), 0)
        for msg in mail.outbox:
            if msg.to[0] == 'joh@doe.com':
                self.assertEqual(msg.subject, 'Activate Your Privalytics Account')

    def test_user_creation(self):
        self.assertTrue(User.objects.filter(email='joh@doe.com').exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_activation(self):
        user = User.objects.get(email='joh@doe.com')
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
        response = self.client.get(reverse('activate', args=(uid, token)))
        self.assertRedirects(response, reverse('dashboard'))

