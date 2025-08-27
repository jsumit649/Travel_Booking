from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Template URLs
    path('', views.home, name='home'),
    path('travel-options/', views.travel_options_view, name='travel-options'),
    path('bookings/', views.bookings_view, name='bookings'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # API URLs
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/login/', views.LoginView.as_view(), name='api-login'),
    path('api/logout/', views.LogoutView.as_view(), name='api-logout'),
    path('api/profile/', views.UserProfileView.as_view(), name='api-profile'),
    
    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Travel Options URLs
    path('api/travel-options/', views.TravelOptionListCreateView.as_view(), name='api-travel-options'),
    path('api/travel-options/<int:travel_id>/', views.TravelOptionDetailView.as_view(), name='api-travel-option-detail'),
    path('api/travel-search/', views.TravelSearchView.as_view(), name='api-travel-search'),
    
    # Booking URLs
    path('api/bookings/', views.BookingListCreateView.as_view(), name='api-bookings'),
    path('api/bookings/<int:booking_id>/', views.BookingDetailView.as_view(), name='api-booking-detail'),
    path('api/bookings/<int:booking_id>/cancel/', views.cancel_booking, name='api-cancel-booking'),
]