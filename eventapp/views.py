from django.shortcuts import render, redirect

from eventapp.models import Event


def allevents(request):
    # Retrieve all events from the database
    events = Event.objects.all()

    # Pass the events to the template context
    context = {'events': events}

    # Render the template with the events
    return render(request, 'eventapp/base/home.html', context)


def addevent(request):
    if request.method == 'POST':
        # Handle the form submission to add a new event
        # Extract the form data and save the event

        return redirect('eventapp:home')  # Redirect to the home page after adding the event

    # If it's a GET request, render the add event form
    return render(request, 'eventapp/base/addevent.html')
