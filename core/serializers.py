from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from .models import UserProfile, TravelOption, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'date_of_birth', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 
                 'phone_number', 'date_of_birth', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        phone_number = validated_data.pop('phone_number')
        date_of_birth = validated_data.pop('date_of_birth', None)
        address = validated_data.pop('address', '')
        
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            address=address
        )
        return user

class TravelOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelOption
        fields = '__all__'
        read_only_fields = ['travel_id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    travel_option = TravelOptionSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'reference_number', 'user', 'travel_option', 'number_of_seats', 
                 'passenger_details', 'total_price', 'booking_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['booking_id', 'reference_number', 'user', 'total_price', 
                           'booking_date', 'created_at', 'updated_at']

class CreateBookingSerializer(serializers.ModelSerializer):
    travel_option = serializers.PrimaryKeyRelatedField(queryset=TravelOption.objects.all())
    
    class Meta:
        model = Booking
        fields = ['travel_option', 'number_of_seats', 'passenger_details']

    def validate(self, attrs):
        travel_option = attrs.get('travel_option')
        number_of_seats = attrs.get('number_of_seats')
        passenger_details = attrs.get('passenger_details', [])
        
        # Basic validation
        if not travel_option:
            raise serializers.ValidationError("Travel option is required.")
        
        if not number_of_seats or number_of_seats <= 0:
            raise serializers.ValidationError("Number of seats must be greater than 0.")
        
        # Check if travel option has departed with specific error message
        try:
            from django.utils import timezone
            now = timezone.now()
            dep_dt = timezone.make_aware(
                timezone.datetime.combine(travel_option.departure_date, travel_option.departure_time),
                timezone=timezone.get_current_timezone()
            )
            if dep_dt < now:
                # Create a more specific error message
                travel_type = travel_option.type.title()
                departure_time = travel_option.get_formatted_departure_time()
                raise serializers.ValidationError(
                    f"The {travel_type} from {travel_option.source} to {travel_option.destination} "
                    f"({travel_option.operator_name}) has already departed at {departure_time}. "
                    f"Please select a different travel option."
                )
        except Exception as e:
            raise serializers.ValidationError(f"Error checking departure time: {str(e)}")
        
        # Check seat availability
        if travel_option.available_seats < number_of_seats:
            raise serializers.ValidationError(
                f"Only {travel_option.available_seats} seats available. You requested {number_of_seats} seats."
            )
        
        # Validate passenger details
        if not isinstance(passenger_details, list):
            raise serializers.ValidationError("Passenger details must be a list.")
        
        if len(passenger_details) != number_of_seats:
            raise serializers.ValidationError(
                f"Number of passenger details ({len(passenger_details)}) must match number of seats ({number_of_seats})."
            )
        
        # Validate each passenger detail
        for i, passenger in enumerate(passenger_details):
            if not isinstance(passenger, dict):
                raise serializers.ValidationError(f"Passenger {i+1} details must be an object.")
            
            # Check required fields
            if 'name' not in passenger or not passenger['name'] or not passenger['name'].strip():
                raise serializers.ValidationError(f"Passenger {i+1} name is required and cannot be empty.")
            
            if 'age' not in passenger:
                raise serializers.ValidationError(f"Passenger {i+1} age is required.")
            
            # Validate age
            try:
                age = int(passenger['age'])
                if age <= 0 or age > 120:
                    raise serializers.ValidationError(f"Passenger {i+1} age must be between 1 and 120.")
            except (ValueError, TypeError):
                raise serializers.ValidationError(f"Passenger {i+1} age must be a valid number.")
        
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        travel_option = validated_data['travel_option']
        number_of_seats = validated_data['number_of_seats']
        passenger_details = validated_data['passenger_details']
        
        try:
            # Use the new create_booking method with seat reservation
            booking = Booking.create_booking(
                user=user,
                travel_option=travel_option,
                number_of_seats=number_of_seats,
                passenger_details=passenger_details
            )
            return booking
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create booking: {str(e)}")
