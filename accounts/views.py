from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from accounts.forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('forum:home')  # TODO sign up redirect url, edit in test also
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def edit_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('forum:home')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def view_profile(request, pk=None):
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user
    return render(request, 'accounts/user_profile.html', {'user': user})