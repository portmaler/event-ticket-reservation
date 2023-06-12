from django.urls import path
from .views import dashboard,home

app_name = 'dashboard'

urlpatterns = [
    path('home/', home, name='home'),
    path('', dashboard, name='index'),
]
