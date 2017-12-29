from django.contrib.auth import login
from django.shortcuts import render, redirect
from accounts.form import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('accounts:login')  # TODO sign up redirect url
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})
