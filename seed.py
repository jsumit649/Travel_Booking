import os
import sys
import django
from datetime import datetime, date, time, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Travel_Booking.settings')
django.setup()

from core.models import TravelOption

def seed_travel_options():
    """Seed the database with travel options for flights, trains, and buses"""
    
    # Clear existing travel options
    TravelOption.objects.all().delete()
    print("Cleared existing travel options...")
    
    # Flight data
    flights = [
        {
            'type': 'flight',
            'operator_name': 'Air India',
            'source': 'Delhi',
            'destination': 'Mumbai',
            'price': 8500.00,
            'total_seats': 180,
            'available_seats': 180,
        },
        {
            'type': 'flight',
            'operator_name': 'IndiGo',
            'source': 'Delhi',
            'destination': 'Bangalore',
            'price': 7200.00,
            'total_seats': 160,
            'available_seats': 160,
        },
        {
            'type': 'flight',
            'operator_name': 'SpiceJet',
            'source': 'Mumbai',
            'destination': 'Delhi',
            'price': 7800.00,
            'total_seats': 140,
            'available_seats': 140,
        },
        {
            'type': 'flight',
            'operator_name': 'Vistara',
            'source': 'Delhi',
            'destination': 'Chennai',
            'price': 9200.00,
            'total_seats': 150,
            'available_seats': 150,
        },
        {
            'type': 'flight',
            'operator_name': 'AirAsia India',
            'source': 'Bangalore',
            'destination': 'Delhi',
            'price': 6800.00,
            'total_seats': 120,
            'available_seats': 120,
        },
        {
            'type': 'flight',
            'operator_name': 'GoAir',
            'source': 'Mumbai',
            'destination': 'Kolkata',
            'price': 6500.00,
            'total_seats': 130,
            'available_seats': 130,
        },
        {
            'type': 'flight',
            'operator_name': 'Air India',
            'source': 'Delhi',
            'destination': 'Kolkata',
            'price': 7500.00,
            'total_seats': 170,
            'available_seats': 170,
        },
        {
            'type': 'flight',
            'operator_name': 'IndiGo',
            'source': 'Chennai',
            'destination': 'Mumbai',
            'price': 8200.00,
            'total_seats': 160,
            'available_seats': 160,
        }
    ]
    
    # Train data
    trains = [
        {
            'type': 'train',
            'operator_name': 'Rajdhani Express',
            'source': 'Delhi',
            'destination': 'Mumbai',
            'price': 2500.00,
            'total_seats': 500,
            'available_seats': 500,
        },
        {
            'type': 'train',
            'operator_name': 'Shatabdi Express',
            'source': 'Delhi',
            'destination': 'Agra',
            'price': 800.00,
            'total_seats': 300,
            'available_seats': 300,
        },
        {
            'type': 'train',
            'operator_name': 'Duronto Express',
            'source': 'Delhi',
            'destination': 'Kolkata',
            'price': 1800.00,
            'total_seats': 450,
            'available_seats': 450,
        },
        {
            'type': 'train',
            'operator_name': 'Garib Rath Express',
            'source': 'Mumbai',
            'destination': 'Delhi',
            'price': 1200.00,
            'total_seats': 600,
            'available_seats': 600,
        },
        {
            'type': 'train',
            'operator_name': 'Rajdhani Express',
            'source': 'Delhi',
            'destination': 'Bangalore',
            'price': 3200.00,
            'total_seats': 480,
            'available_seats': 480,
        },
        {
            'type': 'train',
            'operator_name': 'Sampark Kranti Express',
            'source': 'Delhi',
            'destination': 'Chennai',
            'price': 2800.00,
            'total_seats': 520,
            'available_seats': 520,
        },
        {
            'type': 'train',
            'operator_name': 'Duronto Express',
            'source': 'Mumbai',
            'destination': 'Kolkata',
            'price': 2200.00,
            'total_seats': 400,
            'available_seats': 400,
        },
        {
            'type': 'train',
            'operator_name': 'Shatabdi Express',
            'source': 'Delhi',
            'destination': 'Jaipur',
            'price': 600.00,
            'total_seats': 280,
            'available_seats': 280,
        }
    ]
    
    # Bus data
    buses = [
        {
            'type': 'bus',
            'operator_name': 'RedBus',
            'source': 'Delhi',
            'destination': 'Agra',
            'price': 400.00,
            'total_seats': 45,
            'available_seats': 45,
        },
        {
            'type': 'bus',
            'operator_name': 'Goibibo',
            'source': 'Delhi',
            'destination': 'Jaipur',
            'price': 350.00,
            'total_seats': 40,
            'available_seats': 40,
        },
        {
            'type': 'bus',
            'operator_name': 'MakeMyTrip',
            'source': 'Delhi',
            'destination': 'Chandigarh',
            'price': 500.00,
            'total_seats': 35,
            'available_seats': 35,
        },
        {
            'type': 'bus',
            'operator_name': 'RedBus',
            'source': 'Mumbai',
            'destination': 'Pune',
            'price': 300.00,
            'total_seats': 50,
            'available_seats': 50,
        },
        {
            'type': 'bus',
            'operator_name': 'Goibibo',
            'source': 'Bangalore',
            'destination': 'Mysore',
            'price': 250.00,
            'total_seats': 42,
            'available_seats': 42,
        },
        {
            'type': 'bus',
            'operator_name': 'MakeMyTrip',
            'source': 'Delhi',
            'destination': 'Dehradun',
            'price': 600.00,
            'total_seats': 38,
            'available_seats': 38,
        },
        {
            'type': 'bus',
            'operator_name': 'RedBus',
            'source': 'Chennai',
            'destination': 'Bangalore',
            'price': 450.00,
            'total_seats': 44,
            'available_seats': 44,
        },
        {
            'type': 'bus',
            'operator_name': 'Goibibo',
            'source': 'Kolkata',
            'destination': 'Durgapur',
            'price': 200.00,
            'total_seats': 48,
            'available_seats': 48,
        }
    ]
    
    # Combine all travel options
    all_travel_options = flights + trains + buses
    
    # Generate dates for the next 30 days
    base_date = date.today()
    
    created_count = 0
    
    for option in all_travel_options:
        # Create multiple dates for each route
        for day_offset in range(30):  # Next 30 days
            travel_date = base_date + timedelta(days=day_offset)
            
            # Generate random departure and arrival times
            if option['type'] == 'flight':
                # Flights: 6 AM to 10 PM
                departure_hour = random.randint(6, 22)
                departure_minute = random.choice([0, 15, 30, 45])
                departure_time = time(departure_hour, departure_minute)
                
                # Flight duration: 1-4 hours
                duration_hours = random.randint(1, 4)
                duration_minutes = random.randint(0, 59)
                
                arrival_time = time(
                    (departure_hour + duration_hours) % 24,
                    (departure_minute + duration_minutes) % 60
                )
                
                # If arrival is next day
                if (departure_hour + duration_hours) >= 24:
                    arrival_date = travel_date + timedelta(days=1)
                else:
                    arrival_date = travel_date
                    
            elif option['type'] == 'train':
                # Trains: 5 AM to 11 PM
                departure_hour = random.randint(5, 23)
                departure_minute = random.choice([0, 15, 30, 45])
                departure_time = time(departure_hour, departure_minute)
                
                # Train duration: 2-12 hours
                duration_hours = random.randint(2, 12)
                duration_minutes = random.randint(0, 59)
                
                arrival_time = time(
                    (departure_hour + duration_hours) % 24,
                    (departure_minute + duration_minutes) % 60
                )
                
                # If arrival is next day
                if (departure_hour + duration_hours) >= 24:
                    arrival_date = travel_date + timedelta(days=1)
                else:
                    arrival_date = travel_date
                    
            else:  # Bus
                # Buses: 6 AM to 9 PM
                departure_hour = random.randint(6, 21)
                departure_minute = random.choice([0, 15, 30, 45])
                departure_time = time(departure_hour, departure_minute)
                
                # Bus duration: 2-8 hours
                duration_hours = random.randint(2, 8)
                duration_minutes = random.randint(0, 59)
                
                arrival_time = time(
                    (departure_hour + duration_hours) % 24,
                    (departure_minute + duration_minutes) % 60
                )
                
                # If arrival is next day
                if (departure_hour + duration_hours) >= 24:
                    arrival_date = travel_date + timedelta(days=1)
                else:
                    arrival_date = travel_date
            
            # Create the travel option
            travel_option = TravelOption.objects.create(
                type=option['type'],
                operator_name=option['operator_name'],
                source=option['source'],
                destination=option['destination'],
                departure_date=travel_date,
                departure_time=departure_time,
                arrival_date=arrival_date,
                arrival_time=arrival_time,
                price=option['price'],
                available_seats=option['available_seats'],
                total_seats=option['total_seats']
            )
            
            created_count += 1
            
            # Print progress every 100 records
            if created_count % 100 == 0:
                print(f"Created {created_count} travel options...")
    
    print(f"\n✅ Successfully created {created_count} travel options!")
    print(f"📊 Breakdown:")
    print(f"   - Flights: {len(flights) * 30} options")
    print(f"   - Trains: {len(trains) * 30} options")
    print(f"   - Buses: {len(buses) * 30} options")
    print(f"\n💰 Price Range:")
    print(f"   - Flights: ₹6,500 - ₹9,200")
    print(f"   - Trains: ₹600 - ₹3,200")
    print(f"   - Buses: ₹200 - ₹600")
    print(f"\n🗓️  Date Range: {base_date} to {base_date + timedelta(days=29)}")

if __name__ == "__main__":
    print("🚀 Starting to seed travel options...")
    seed_travel_options()
    print("\n🎉 Seeding completed successfully!")
