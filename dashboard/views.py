from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
   # return render(request, 'authentification/dashboard.html', context=context)
    return render(request, 'base/base.html', context=context)

'''@login_required
def dashboard(request):
    welcome_message = "Welcome to your dashboard"
    return HttpResponse(welcome_message)'''
