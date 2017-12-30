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
    path('reset-password/', auth_views.password_reset, {'post_reset_redirect': 'accounts:password_reset_done',
                                                       'email_template_name': 'accounts/password_reset_email.html',
                                                       'template_name': 'accounts/password_reset.html'},
         name='password_reset'),
    path('reset-password/done/', auth_views.password_change_done, {'template_name': 'accounts/password_reset_done.html'},
         name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9a-zA-Z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
            {'post_reset_redirect': 'accounts:password_reset_complete',
             'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.password_reset_complete,
         {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
]
