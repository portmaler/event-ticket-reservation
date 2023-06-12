from django.urls import path
from .views import allevents, addevent

app_name = 'eventapp'

urlpatterns = [
    path('events/', allevents, name='home'),
    path('', addevent, name='index'),
]
