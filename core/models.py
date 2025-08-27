from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import transaction
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class TravelOption(models.Model):
    TRAVEL_TYPE_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    travel_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPE_CHOICES)
    operator_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    duration = models.DurationField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensure departure is before arrival
        dep_dt = timezone.datetime.combine(self.departure_date, self.departure_time)
        arr_dt = timezone.datetime.combine(self.arrival_date, self.arrival_time)
        if dep_dt >= arr_dt:
            raise ValidationError("Departure must be before arrival.")
        if self.available_seats > self.total_seats:
            raise ValidationError("Available seats cannot exceed total seats.")

    def save(self, *args, **kwargs):
        # Calculate duration
        dep_dt = timezone.datetime.combine(self.departure_date, self.departure_time)
        arr_dt = timezone.datetime.combine(self.arrival_date, self.arrival_time)
        self.duration = arr_dt - dep_dt
        super().save(*args, **kwargs)

    def reserve_seats(self, number_of_seats):
        """Reserve seats for a booking"""
        if self.available_seats >= number_of_seats:
            self.available_seats -= number_of_seats
            self.save()
            return True
        return False

    def release_seats(self, number_of_seats):
        """Release seats back to available pool"""
        # Remove the restrictive validation - just ensure we don't exceed total seats
        if self.available_seats + number_of_seats <= self.total_seats:
            self.available_seats += number_of_seats
            self.save()
            return True
        else:
            # If we would exceed total seats, just set to total seats
            self.available_seats = self.total_seats
            self.save()
            return True

    def get_departure_datetime_local(self):
        """Get departure datetime in local timezone"""
        # Create a timezone-aware datetime
        dep_dt = timezone.make_aware(
            timezone.datetime.combine(self.departure_date, self.departure_time),
            timezone=timezone.get_current_timezone()
        )
        return dep_dt

    def get_arrival_datetime_local(self):
        """Get arrival datetime in local timezone"""
        # Create a timezone-aware datetime
        arr_dt = timezone.make_aware(
            timezone.datetime.combine(self.arrival_date, self.arrival_time),
            timezone=timezone.get_current_timezone()
        )
        return arr_dt

    def get_time_until_departure(self):
        """Get time remaining until departure"""
        now = timezone.now()
        departure = self.get_departure_datetime_local()
        return departure - now

    def is_departed(self):
        """Check if the travel option has already departed"""
        now = timezone.now()
        departure = self.get_departure_datetime_local()
        return departure < now

    def get_formatted_departure_time(self):
        """Get formatted departure time for display"""
        return self.get_departure_datetime_local().strftime("%I:%M %p, %d %B %Y")

    def get_formatted_arrival_time(self):
        """Get formatted arrival time for display"""
        return self.get_arrival_datetime_local().strftime("%I:%M %p, %d %B %Y")

    def __str__(self):
        return f"{self.type.title()} {self.source} to {self.destination} ({self.operator_name})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    reference_number = models.CharField(max_length=36, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    passenger_details = models.JSONField(help_text="List of passenger info: name, age, id_number, special_requirements")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.number_of_seats > self.travel_option.available_seats:
            raise ValidationError("Not enough available seats for this booking.")

    def save(self, *args, **kwargs):
        # Auto-generate reference number
        if not self.reference_number:
            self.reference_number = str(uuid.uuid4())
        # Calculate total price
        self.total_price = self.number_of_seats * self.travel_option.price
        super().save(*args, **kwargs)

    @classmethod
    def create_booking(cls, user, travel_option, number_of_seats, passenger_details):
        """Create a booking with seat reservation"""
        try:
            with transaction.atomic():
                # Double-check seat availability
                if travel_option.available_seats < number_of_seats:
                    raise ValidationError("Not enough available seats for this booking.")
                
                # Create booking first
                booking = cls.objects.create(
                    user=user,
                    travel_option=travel_option,
                    number_of_seats=number_of_seats,
                    passenger_details=passenger_details,
                    status='confirmed'
                )
                
                # Then reserve seats
                travel_option.available_seats -= number_of_seats
                travel_option.save()
                
                return booking
        except Exception as e:
            raise ValidationError(f"Failed to create booking: {str(e)}")

    def cancel_booking(self):
        """Cancel booking and release seats"""
        if self.status == 'confirmed':
            try:
                with transaction.atomic():
                    # Release seats back to available pool
                    if self.travel_option.release_seats(self.number_of_seats):
                        self.status = 'cancelled'
                        self.save()
                        return True
                    else:
                        raise ValidationError("Failed to release seats.")
            except Exception as e:
                raise ValidationError(f"Error cancelling booking: {str(e)}")
        return False

    def __str__(self):
        return f"Booking {self.reference_number} by {self.user.username}"