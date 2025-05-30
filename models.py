from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='No description available')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_types/', null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add default value
    description = models.TextField(default='No description available')
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.room_type.name} - {self.price}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"

    def is_active(self):
        today = date.today()
        return self.check_in_date <= today <= self.check_out_date and not self.is_cancelled

    def save(self, *args, **kwargs):
        # Calculate total price based on number of nights and room type price
        nights = (self.check_out_date - self.check_in_date).days
        self.total_price = nights * self.room.room_type.price_per_night
        super().save(*args, **kwargs)

from django.contrib.auth.models import User

class Customer(User):
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'