from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from dashboard.forms import EventForm


def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
   # return render(request, 'authentification/dashboard.html', context=context)
    return render(request, 'dashboard/base/dashboard.html', context=context)
def managerdashboard(request):

   # return render(request, 'authentification/dashboard.html', context=context)
    return render(request, 'dashboard/manager/dashboard.html')
def home(request):
    return render(request, 'dashboard/base/home.html')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            # You can perform additional actions if needed
            return redirect('managerdashboard')  # Replace 'managerdashboard' with your desired URL name
    else:
        form = EventForm()
    return render(request, 'dashboard/manager/add-event.html', {'form': form})


'''@login_required
def dashboard(request):
    welcome_message = "Welcome to your dashboard"
    return HttpResponse(welcome_message)'''
