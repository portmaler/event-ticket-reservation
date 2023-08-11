from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from eventapp.models import Event, Ticket, Reservation, Coupon


def allevents(request):
    # Retrieve all events from the database
    events = Event.objects.filter(is_confirmed=True).all()
    recent_events = Event.objects.order_by('-date')[:3]

    # Pass the events to the template context
    context = {'events': events, 'recent_events': recent_events}

    # Render the template with the events
    return render(request, 'eventapp/home.html', context)


"""def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket = Ticket.objects.filter(event=event, user=request.user).first()  # Assuming the user is logged in
    reservation = Reservation.objects.filter(user=request.user, tickets__event=event).first()  # Assuming the user is logged in
    context = {
        'event': event,
        'ticket': ticket,
        'reservation': reservation
    }
    return render(request, 'eventapp/event_detail.html', context)"""


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket = Ticket.objects.filter(event=event).first()  # Assuming the user is logged in

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        if quantity <= event.tickets_available:
            coupon_code = request.POST.get('coupon_code', '')
            coupon = Coupon.objects.filter(code=coupon_code).first()
            if coupon:
                total_price = (ticket.price * quantity) - coupon.discount_amount
            else:
                total_price = ticket.price * quantity

            reservation = Reservation.objects.create(user=request.user, total_price=total_price)
            # Update event tickets_available count
            event.tickets_available -= quantity
            reservation.save()
            event.save()
            return redirect('eventapp:ticket-confirmation', ticket_id=ticket.id)
        else:
            # Handle insufficient tickets error
            error_message = 'Insufficient tickets available'
            return render(request, 'eventapp/event_detail.html',
                          {'event': event, 'ticket': ticket, 'error_message': error_message})

    context = {
        'event': event,
        'ticket': ticket,
    }
    return render(request, 'eventapp/event_detail.html', context)


def ticket_confirmation(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    event = ticket.event
    context = {
        'ticket': ticket,
        'event': event,
    }
    return render(request, 'eventapp/ticket-confirmation.html', context)


def category_events(request, category):
    # Retrieve events based on the clicked category
    events = Event.objects.filter(is_confirmed=True,category=category)
    context = {
        'events': events,
    }
    return render(request, 'eventapp/category_events.html', context)


def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Handle the form submission and update the event data
        # ...

        messages.success(request, 'Event updated successfully.')
        return redirect('event_detail', event_id=event.id)

    context = {
        'event': event,
    }
    return render(request, 'dashboard/event_edit.html', context)


def event_confirm_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Delete the event
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('dashboard')  # Redirect to the dashboard or any desired page

    context = {
        'event': event,
    }
    return render(request, 'dashboard/event_confirm_delete.html', context)
