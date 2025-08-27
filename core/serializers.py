from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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
    class Meta:
        model = Booking
        fields = ['travel_option', 'number_of_seats', 'passenger_details']
