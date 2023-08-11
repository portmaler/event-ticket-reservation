import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.forms import EventForm, UserForm, TicketForm
from eventapp.models import Ticket, Coupon, Reservation
from eventapp.models import Event
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# ************** Admin


@login_required(login_url='authentification:login')
def admin_dashboard(request):
    users = User.objects.filter(is_staff=True)
    events = Event.objects.filter(user__is_staff=True, is_confirmed=False)
    tickets_sold = Reservation.objects.count()
    total_events = Event.objects.filter(user__is_staff=True).count()
    current_datetime = datetime.now()
    upcoming_tickets = Ticket.objects.filter(event__user__is_staff=True, reservation_date__gt=current_datetime).count()
    expired_tickets = Ticket.objects.filter(event__user__is_staff=True, reservation_date__lt=current_datetime).count()

    context = {
        'users': users,
        'events': events,
        'tickets_sold': tickets_sold,
        'total_events': total_events,
        'upcoming_tickets': upcoming_tickets,
        'expired_tickets': expired_tickets
    }

    return render(request, 'dashboard/admin/dashboard.html', context)


@login_required(login_url='authentification:login')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:admin-dashboard')
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'dashboard/admin/add-user.html', context)


@login_required(login_url='authentification:login')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    users = User.objects.exclude(id=user_id)

    if request.method == "POST":
        is_staff = request.POST.get('is_staff') == '1'  # Check if the radio button value is '1'

        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = is_staff
            user.email = form.cleaned_data['email']  # Update the email field
            user.save()
            return redirect('dashboard:admin-dashboard')
    else:
        form = UserChangeForm(instance=user, initial={'email': user.email})  # Set initial email value

    context = {
        'form': form,
        'users': users
    }
    return render(request, 'dashboard/admin/edit-user.html', context)


@login_required(login_url='authentification:login')
def confirm_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        event.is_confirmed = True
        event.save()
        return redirect('dashboard:admin-dashboard')
    else:
        return render(request, 'dashboard/admin/dashboard.html')


# ************** Manager
@login_required(login_url='authentification:login')
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    # return render(request, 'authentification/dashboard.html', context=context)
    return render(request, 'dashboard/base/dashboard.html', context=context)


@login_required(login_url='authentification:login')
def manager_dashboard(request):
    user = request.user
    events = Event.objects.filter(user=user)
    tickets = Ticket.objects.filter(event__in=events)
    return render(request, 'dashboard/manager/dashboard.html', {'events': events, 'tickets': tickets})


@login_required(login_url='authentification:login')
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # Set the current user as the event's user
            event.save()
            return redirect('dashboard:manager-dashboard')
    else:
        form = EventForm()
    return render(request, 'dashboard/manager/add-event.html', {'form': form})


@login_required(login_url='authentification:login')
def add_ticket(request):
    # Retrieve events for the connected user
    events = Event.objects.filter(user=request.user)
    coupons = Coupon.objects.filter(user=request.user)  # Retrieve coupons for the connected user

    if request.method == 'POST':
        event_id = request.POST['event']
        quantity = request.POST['quantity']
        price = request.POST['price']
        coupon_id = request.POST['coupon']  # Get the selected coupon ID

        event = Event.objects.get(id=event_id)

        ticket = Ticket(event=event, user=request.user, quantity=quantity, price=price, coupon_id=coupon_id)
        ticket.save()

        return redirect('dashboard:manager-dashboard')

    # Pass the events and coupons to the template context
    context = {'events': events, 'coupons': coupons}

    return render(request, 'dashboard/manager/add-ticket.html', context)


@login_required(login_url='authentification:login')
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect(
                'dashboard:manager-dashboard')  # Replace 'dashboard:ticket-list' with your actual URL name for the ticket list page
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'ticket': ticket,
    }
    return render(request, 'dashboard/manager/edit-ticket.html', context)


@login_required(login_url='authentification:login')
def event_edit(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('dashboard:manager-dashboard')
    else:
        form = EventForm(instance=event)

    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'dashboard/manager/edit-event.html', context)


@login_required(login_url='authentification:login')
def event_edit_dash(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    if request.method == 'POST':
        # Process the form data
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    # GET request
    form = EventForm(instance=event)
    events = Event.objects.filter(user=request.user).values('id', 'title', 'date', 'time', 'location', 'category')

    context = {
        'form': form,
        'events_json': json.dumps({event['id']: event for event in events}),
    }

    return render(request, 'dashboard/manager/event-edit-dash.html', context)


@login_required(login_url='authentification:login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        # Redirect to the dashboard or any other page after successful deletion
        return redirect('dashboard:manager-dashboard')

    # Handle GET request or any other method
    # Render a confirmation template or perform any other desired action
    return render(request, 'dashboard/delete_confirmation.html', {'event': event})


# views.py
@login_required(login_url='authentification:login')
def add_coupon(request):
    if request.method == 'POST':
        title = request.POST['title']
        code = request.POST['code']
        discount_amount = request.POST['discount_amount']

        coupon = Coupon(user=request.user, code=code, discount_amount=discount_amount, title=title)
        coupon.save()

        return redirect('dashboard:manager-dashboard')

    return render(request, 'dashboard/manager/add-coupon.html')


# views.py
@login_required(login_url='authentification:login')
def edit_coupon(request):
    # Retrieve coupons for the current user
    coupons = Coupon.objects.filter(user=request.user)

    if request.method == 'POST':
        coupon_id = request.POST['coupon']
        code = request.POST['code']
        discount_amount = request.POST['discount_amount']

        coupon = Coupon.objects.get(id=coupon_id)
        coupon.code = code
        coupon.discount_amount = discount_amount
        coupon.save()

        return redirect('dashboard:manager-dashboard')

    context = {'coupons': coupons}
    return render(request, 'dashboard/manager/edit-coupon.html', context)
