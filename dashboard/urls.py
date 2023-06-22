from django.urls import path
from .views import dashboard, home, addevent, managerdashboard

app_name = 'dashboard'

urlpatterns = [
    path('home/', home, name='home'),
    path('manager/', managerdashboard, name='manager-dashboard'),
   # path('', dashboard, name='index'),
    path('addevent', addevent, name='add-event'),
]
