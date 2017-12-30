from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth import views as auth_views
from django.contrib.auth import forms as auth_forms


class LoginViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('accounts:login'))

    def test_sigup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.view_class, auth_views.LoginView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, auth_forms.AuthenticationForm)

    def test_forms_input(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 1)


class SuccessfulLoginTests(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test_user',
            'password': 'testpassword1234',
        }
        User.objects.create_user(**self.user_credentials)
        self.response = self.client.post(reverse('accounts:login'), self.user_credentials, follow=True)
        self.login_redirect_url = reverse('forum:home')

    def test_login(self):
        self.assertTrue(self.response.context['user'].is_active)

    def test_login_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_redirects_to_redirect_url(self):
        self.assertRedirects(self.response, self.login_redirect_url)


class InvalidLoginTests(TestCase):
    def setUp(self):
        self.user_credentials = {
            'username': 'test_user',
            'password': 'testpassword1234',
        }
        self.response = self.client.post(reverse('accounts:login'), self.user_credentials)

    def test_login_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login(self):
        self.assertFalse(self.response.context['user'].is_active)

    def test_non_field_errors(self):
        self.assertTrue(self.response.context['form'].non_field_errors)
