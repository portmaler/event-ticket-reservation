from django.urls import path
from .views import add_event, manager_dashboard, add_ticket, event_edit, delete_event, admin_dashboard, \
    confirm_event, add_coupon, edit_coupon, add_user, edit_user, event_edit_dash, ticket_edit

app_name = 'dashboard'

urlpatterns = [

    path('admin/', admin_dashboard, name='admin-dashboard'),
    path('admin/confirm-event/<int:event_id>/', confirm_event, name='confirm-event'),
    path('admin/add-user/', add_user, name='add-user'),
    path('admin/edit-user/<int:user_id>/', edit_user, name='edit-user'),



    path('addevent/', add_event, name='add-event'),
    path('addticket/', add_ticket, name='add-ticket'),
    path('editevent/<int:event_id>/', event_edit, name='event-edit'),
    path('editticket/<int:event_id>/', ticket_edit, name='ticket-edit'),
    path('editeventdash/<int:event_id>/', event_edit_dash, name='event-edit-dash'),
    path('manager/', manager_dashboard, name='manager-dashboard'),
    path('delevent/<int:event_id>/', delete_event, name='event-delete'),  # Add this line

    # Add Coupon
    path('addcoupon/', add_coupon, name='add-coupon'),

    # Edit Coupon
    path('editcoupon/', edit_coupon, name='edit-coupon'),
   # path('', dashboard, name='index'),



]
