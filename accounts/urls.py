from django.urls import path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),
    path('signup/', accounts_views.signup, name='signup'),
    path('edit-profile', accounts_views.edit_profile, name='edit_profile')
]
