import os
import sys
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Travel_Booking.settings')
django.setup()

from core.models import TravelOption, Booking, User
from core.serializers import CreateBookingSerializer
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User

def test_booking_creation():
    """Test booking creation to debug the 400 error"""
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Get a travel option with available seats
    travel_option = TravelOption.objects.filter(available_seats__gt=0).first()
    
    if not travel_option:
        print("❌ No travel options with available seats found!")
        return
    
    print(f"✅ Testing with travel option: {travel_option}")
    print(f"   Available seats: {travel_option.available_seats}")
    print(f"   Departure: {travel_option.departure_date} at {travel_option.departure_time}")
    
    # Test data - use travel_option ID instead of object
    test_data = {
        'travel_option': travel_option.travel_id,  # Use ID instead of object
        'number_of_seats': 1,
        'passenger_details': [
            {
                'name': 'John Doe',
                'age': 30,
                'id_number': 'ID123456',
                'special_requirements': 'None'
            }
        ]
    }
    
    # Create a mock request
    factory = APIRequestFactory()
    request = factory.post('/api/bookings/')
    request.user = user
    
    # Test serializer validation
    serializer = CreateBookingSerializer(data=test_data, context={'request': request})
    
    print("\n Testing serializer validation...")
    if serializer.is_valid():
        print("✅ Serializer validation passed")
        
        try:
            booking = serializer.save()
            print(f"✅ Booking created successfully: {booking.reference_number}")
            print(f"   Seats after booking: {travel_option.available_seats}")
        except Exception as e:
            print(f"❌ Error creating booking: {e}")
    else:
        print("❌ Serializer validation failed:")
        for field, errors in serializer.errors.items():
            print(f"   {field}: {errors}")

if __name__ == "__main__":
    test_booking_creation()
