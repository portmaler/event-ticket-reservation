from django.urls import path
from .views import edit,  register
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetDoneView)

app_name = 'authentification'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
   # path('dashboard/', 'dashboard.dashboard', name='dashboard'),
    path('login', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='authentification/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authentification/password_change_form.html'), name='password_change'),
    path('password_change/dond/', PasswordChangeDoneView.as_view(template_name='authentification/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authentification/password_reset_form.html',
        email_template_name='authentification/password_reset_email.html',
        success_url=reverse_lazy('authentification:password_reset_done')), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='authentification/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='authentification/password_reset_confirm.html',
        success_url=reverse_lazy('authentification:login')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='authentification/password_reset_complete.html'), name='password_reset_complete'),

]