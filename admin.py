from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import RoomType, Room, Booking, Customer

# Unregister the default User admin
admin.site.unregister(User)

# Register the User model with custom admin
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'capacity')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type', 'price', 'description']
    list_filter = ('room_type',)
    search_fields = ('room_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'total_price', 'is_cancelled')
    list_filter = ('is_cancelled', 'room__room_type')
    search_fields = ('user__username', 'room__room_number')
    date_hierarchy = 'check_in_date'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_staff=False, is_superuser=False)  # Only show regular users
