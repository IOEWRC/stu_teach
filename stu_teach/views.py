from django.shortcuts import render


def landing_page(request):
    return render(request, 'registration_redux/landingpage.html')