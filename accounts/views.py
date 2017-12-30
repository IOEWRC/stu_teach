from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from accounts.forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm


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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('accounts:logout')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html',{'form': form})