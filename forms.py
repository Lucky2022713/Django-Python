from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Room
from django.core.exceptions import ValidationError
from datetime import date

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'guests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        guests = cleaned_data.get('guests')
        room = cleaned_data.get('room')

        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError("Check-in date cannot be in the past.")
            if check_out <= check_in:
                raise ValidationError("Check-out date must be after check-in date.")
            
            # Check room availability
            if room and Booking.objects.filter(
                room=room,
                is_cancelled=False,
                check_in_date__lt=check_out,
                check_out_date__gt=check_in
            ).exists():
                raise ValidationError("This room is not available for the selected dates.")

        if room and guests:
            if guests > room.room_type.capacity:
                raise ValidationError(f"This room can accommodate only {room.room_type.capacity} guests.")
        
        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'price', 'description', 'image']