from django.urls import path
from .views import allevents, event_detail, ticket_confirmation, category_events

app_name = 'eventapp'

urlpatterns = [
    path('', allevents, name='home'),
    path('event/<int:event_id>/', event_detail, name='event-detail'),
    path('ticket-confirmation/<int:ticket_id>/', ticket_confirmation, name='ticket-confirmation'),
    path('category/<str:category>/', category_events, name='category-events'),
]


