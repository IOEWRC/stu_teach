from django.urls import path, re_path, reverse_lazy
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),
    path('signup/', accounts_views.signup, name='signup'),
    path('edit-profile/', accounts_views.edit_profile, name='edit_profile'),
    path('profile/edit-profile/', accounts_views.edit_profile, name='edit_profile'),
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9a-zA-Z]+)-(?P<token>.+)/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html',
                success_url=reverse_lazy('accounts:password_reset_complete')
            ), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
