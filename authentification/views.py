from django.contrib.auth.views import LoginView
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import UserRegistration, UserEditForm

# Create your views here.

'''@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
   # return render(request, 'authentification/dashboard.html', context=context)
    return render(request, 'home.html', context=context)'''


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authentification/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authentification/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authentification/edit.html', context=context)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            # Redirect superuser to the admin dashboard
            return reverse_lazy('dashboard:admin-dashboard')
        elif user.is_staff:
            # Redirect staff members to the manager dashboard
            return reverse_lazy('dashboard:manager-dashboard')
        else:
            # Redirect regular users to the home page
            return reverse_lazy('eventapp:home')
