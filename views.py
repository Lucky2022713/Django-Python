from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, RoomType, Booking
from .forms import UserRegistrationForm, BookingForm, RoomForm
from datetime import date, datetime
from django.contrib.auth.models import User

def home(request):
    room_types = RoomType.objects.all()
    return render(request, 'resort/home.html', {'room_types': room_types})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'resort/room_list.html', {'rooms': rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'resort/room_detail.html', {'room': room})

@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'resort/room_form.html', {'form': form})

@login_required
def booking_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        try:
            # Convert string dates to datetime.date objects
            check_in_date = datetime.strptime(request.POST.get('check_in_date'), '%Y-%m-%d').date()
            check_out_date = datetime.strptime(request.POST.get('check_out_date'), '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'resort/room_book.html', {
                'room': room,
                'error': 'Invalid date format. Please select valid dates.'
            })

        # Check if the check-in date is in the past
        if check_in_date < date.today():
            return render(request, 'resort/room_book.html', {
                'room': room,
                'error': 'Check-in date cannot be in the past.'
            })

        # Validate that check-out date is after check-in date
        if check_out_date <= check_in_date:
            return render(request, 'resort/room_book.html', {
                'room': room,
                'error': 'Check-out date must be after check-in date.'
            })

        # Calculate the total price based on the number of nights
        nights = (check_out_date - check_in_date).days
        total_price = nights * room.room_type.price_per_night

        # Create the booking
        booking = Booking.objects.create(
            room=room,
            user=request.user,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guests=int(request.POST.get('guests')),
            total_price=total_price
        )
        return redirect('booking_detail', booking_id=booking.id)
    return render(request, 'resort/room_book.html', {'room': room})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-check_in_date')
    return render(request, 'resort/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'resort/booking_detail.html', {'booking': booking})

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.check_in_date > date.today():
        booking.is_cancelled = True
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel booking after check-in date.')
    
    return redirect('booking_list')

@login_required
def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'resort/room_book.html', {'room': room})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'resort/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'resort/register.html', {'form': form})

@login_required
def customer_list(request):
    customers = User.objects.all()
    return render(request, 'resort/customer_list.html', {'customers': customers})

def room_book(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'resort/room_book.html', {'room': room})