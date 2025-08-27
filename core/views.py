from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile, TravelOption, Booking
from .serializers import (
    UserSerializer, UserProfileSerializer, RegisterSerializer, 
    TravelOptionSerializer, BookingSerializer, CreateBookingSerializer
)
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta

# Template Views
def home(request):
    return render(request, 'core/home.html')

# Add these template views to your existing views.py file

def travel_options_view(request):
    return render(request, 'core/travel_options.html')

@login_required
def bookings_view(request):
    return render(request, 'core/bookings.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'core/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                date_of_birth=date_of_birth if date_of_birth else None,
                address=address
            )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'core/register.html')
    
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update user profile
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        profile.phone_number = request.POST.get('phone_number', '')
        profile.date_of_birth = request.POST.get('date_of_birth') or None
        profile.address = request.POST.get('address', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    # Get booking statistics
    user_bookings = Booking.objects.filter(user=request.user)
    context = {
        'total_bookings': user_bookings.count(),
        'confirmed_bookings': user_bookings.filter(status='confirmed').count(),
        'pending_bookings': user_bookings.filter(status='pending').count(),
    }
    
    return render(request, 'core/profile.html', context)

# API Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                serializer = UserSerializer(user)
                return Response({
                    'message': 'Login successful',
                    'user': serializer.data
                })
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class TravelOptionListCreateView(generics.ListCreateAPIView):
    queryset = TravelOption.objects.all()
    serializer_class = TravelOptionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'source', 'destination', 'departure_date']
    search_fields = ['operator_name', 'source', 'destination']
    ordering_fields = ['price', 'departure_date', 'departure_time']
    ordering = ['departure_date', 'departure_time']

class TravelOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TravelOption.objects.all()
    serializer_class = TravelOptionSerializer
    lookup_field = 'travel_id'

class BookingListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBookingSerializer
        return BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        if booking.status == 'confirmed':
            booking.status = 'cancelled'
            booking.save()
            
            # Update available seats
            travel_option = booking.travel_option
            travel_option.available_seats += booking.number_of_seats
            travel_option.save()
            
            return Response({'message': 'Booking cancelled successfully'})
        else:
            return Response({'error': 'Booking cannot be cancelled'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, 
                       status=status.HTTP_404_NOT_FOUND)

# Search and Filter Views
class TravelSearchView(generics.ListAPIView):
    serializer_class = TravelOptionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = TravelOption.objects.all()
        
        # Get query parameters
        travel_type = self.request.query_params.get('type', None)
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        # Apply filters
        if travel_type:
            queryset = queryset.filter(type=travel_type)
        if source:
            queryset = queryset.filter(source__icontains=source)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date_from:
            queryset = queryset.filter(departure_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(departure_date__lte=date_to)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset.filter(available_seats__gt=0)