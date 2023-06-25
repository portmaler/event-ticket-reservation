from django.urls import path
from .views import edit, register, CustomLoginView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordChangeView, PasswordChangeDoneView
)

app_name = 'authentification'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='authentification/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='authentification/password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='authentification/password_change_done.html'), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authentification/password_reset_form.html',
        email_template_name='authentification/password_reset_email.html',
        success_url='/authentification/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='authentification/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authentification/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='authentification/password_reset_complete.html'), name='password_reset_complete'),
]
