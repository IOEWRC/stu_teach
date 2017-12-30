from django.urls import resolve, reverse
from django.test import TestCase
from accounts.forms import SignupForm
from django.contrib.auth.models import User
from accounts.views import signup


class SignUpViewTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('accounts:signup'))

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SignupForm)

    def test_form_inputs(self):
        """
                The view must contain five inputs: csrf, username, email,
                password1, password2
                :return:
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        self.response = self.client.post(reverse('accounts:signup'), {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'testpassword1234',
            'password2': 'testpassword1234',
        })
        self.sign_up_redirect_url = reverse('accounts:login')

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 302)

    def test_redirects_to_redirect_url(self):
        self.assertRedirects(self.response, self.sign_up_redirect_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(reverse('accounts:edit_profile'))  # TODO better use sign up redirect url
        user = response.context['user']
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        self.response = self.client.post(reverse('accounts:signup'), {})  # a invalid signup; empty dict

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.error_messages)

    def test_no_user_creation(self):
        self.assertFalse(User.objects.exists())