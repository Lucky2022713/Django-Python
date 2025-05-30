from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('book/<int:room_id>/', views.booking_form, name='booking_form'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('customers/', views.customer_list, name='customer_list'),
    path('room/<int:pk>/book/', views.room_book, name='room_book'),
    path('bookings/create/<int:room_id>/', views.booking_create, name='booking_create'),
]