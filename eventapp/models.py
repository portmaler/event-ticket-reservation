from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Event(models.Model):
    CATEGORY_CHOICES = (
        ('concert', 'Concert'),
        ('theater', 'Theater'),
        ('formation', 'Formation'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='theater')
    image = models.ImageField(default='default/blankimage.jpg', upload_to='event_images/')
    is_deleted = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tickets_available = models.IntegerField(default=100)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Custom delete method to set the is_deleted flag instead of actually deleting the event
        self.is_deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Coupon(models.Model):
    title = models.CharField(max_length=100,default="abonnement-client")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=5)
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reservation_date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    reservation_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Reservation - {self.reservation_date}"
