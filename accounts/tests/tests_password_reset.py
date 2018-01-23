from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('accounts:password_reset'))

    def test_password_reset_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PasswordResetForm)

    def test_url_resolves_to_view_function(self):
        view = resolve(reverse('accounts:password_reset'))
        self.assertEqual(view.func, auth_views.password_reset)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_user12345',
        }
        User.objects.create_user(**self.user_credentials)
        self.response = self.client.post(reverse('accounts:password_reset'), {
            'email': self.user_credentials['email']
        })

    def test_redirection(self):
        self.assertRedirects(
            self.response,
            reverse('accounts:password_reset_done'),
            status_code=302,
            target_status_code=302
        )

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        self.response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'hawa@mail.com',
        })

    def test_redirection(self):
        self.assertRedirects(
            self.response,
            reverse('accounts:password_reset_done'),
            status_code=302,
            target_status_code=302
        )

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
