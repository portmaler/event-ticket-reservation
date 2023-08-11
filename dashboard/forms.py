from eventapp.models import Event, Ticket
from django import forms
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'image', 'category', 'tickets_available']



class UserForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_staff']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'user', 'quantity', 'price',  'coupon']


