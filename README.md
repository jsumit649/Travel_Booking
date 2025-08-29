# Travel Booking System

A comprehensive Django-based travel booking system that allows users to search, book, and manage flight, train, and bus reservations with real-time seat availability tracking.

## Features

### 🎯 Core Features
- **Multi-modal Travel**: Support for flights, trains, and buses
- **Real-time Search**: Filter by type, source, destination, date, and price
- **Seat Management**: Real-time seat availability tracking
- **User Authentication**: Registration, login, and profile management
- **Booking Management**: Create, view, and cancel bookings
- **JWT Authentication**: Secure API access with token-based authentication

### 🔧 Technical Features
- **REST API**: Complete API endpoints for all operations
- **Admin Interface**: Django admin panel for managing travel options
- **Responsive UI**: Mobile-friendly web interface
- **Database**: MySQL database with optimized queries
- **Validation**: Comprehensive data validation and error handling

## Tech Stack

- **Backend**: Django 5.2.5, Django REST Framework
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **API Documentation**: RESTful API endpoints

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- MySQL Workbench (recommended)
- pip (Python package installer)
- virtualenv (recommended)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Travel_Booking
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. MySQL Database Setup

Create a database named `travelbooking` and a user with privileges. Example:

```sql
CREATE DATABASE travelbooking;
CREATE USER 'your_db_user'@'%' IDENTIFIED BY 'your_db_password';
GRANT ALL PRIVILEGES ON travelbooking.* TO 'your_db_user'@'%';
FLUSH PRIVILEGES;
```

### 5. Environment Configuration

Edit `.env` in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.mysql
DB_NAME=travelbooking
DB_USER=yourusername
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306

JWT_ACCESS_TOKEN_LIFETIME=1
JWT_REFRESH_TOKEN_LIFETIME=24
```

### 6. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Seed Database with Sample Data

```bash
python seed.py
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## API Endpoints

### Authentication
- `POST /api/register/` — Register a new user
- `POST /api/login/` — Login and get user info
- `POST /api/logout/` — Logout user
- `GET/PUT /api/profile/` — Get or update user profile
- `POST /api/token/` — Get JWT token
- `POST /api/token/refresh/` — Refresh JWT token

### Travel Options
- `GET /api/travel-options/` — List all travel options (filterable)
- `POST /api/travel-options/` — Create travel option (admin)
- `GET /api/travel-options/<travel_id>/` — Get, update, or delete a travel option
- `GET /api/travel-search/` — Search travel options with filters

### Bookings
- `GET /api/bookings/` — List your bookings
- `POST /api/bookings/` — Create a new booking
- `GET /api/bookings/<booking_id>/` — Get, update, or delete a booking
- `POST /api/bookings/<booking_id>/cancel/` — Cancel a booking

### Search Parameters
- `type`: flight, train, bus
- `source`: departure city
- `destination`: arrival city
- `date_from` & `date_to`: date range (YYYY-MM-DD)
- `min_price` & `max_price`: price range

## Usage Examples

### Register a User

```json
POST /api/register/
{
  "username": "sumit",
  "email": "sumit@example.com",
  "password": "StrongPassword123",
  "password2": "StrongPassword123",
  "first_name": "Sumit",
  "last_name": "Kumar",
  "phone_number": "9876543210",
  "date_of_birth": "2000-01-01",
  "address": "Noida, India"
}
```

### Login

```json
POST /api/login/
{
  "username": "sumit",
  "password": "StrongPassword123"
}
```

### Create a Booking

```json
POST /api/bookings/
{
  "travel_option": 1,
  "number_of_seats": 2,
  "passenger_details": [
    {
      "name": "John Doe",
      "age": 30
    },
    {
      "name": "Jane Doe",
      "age": 28
    }
  ]
}
```

### Cancel a Booking

```http
POST /api/bookings/5/cancel/
```

### Search Travel Options

```http
GET /api/travel-search/?type=flight&source=Delhi&destination=Mumbai&date_from=2025-09-01
```

## Admin Panel

Access at `http://127.0.0.1:8000/admin/` using your superuser credentials.

## Project Structure

```
Travel_Booking/
├── Travel_Booking/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
│   └── templates/core/
├── templates/
├── static/
├── seed.py
├── manage.py
└── requirements.txt
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Verify MySQL is running and accessible
   - Check credentials in `.env`
   - Ensure database exists and user has privileges

2. **Migration Issues**
   - Delete migration files (keep `__init__.py`)
   - Run `python manage.py makemigrations`
   - Run `python manage.py migrate`

3. **Import Errors**
   - Activate virtual environment
   - Install missing packages

4. **Permission Denied**
   - Check MySQL user permissions
   - Grant privileges

### Database Reset

```bash
DROP DATABASE travelbooking;
CREATE DATABASE travelbooking;
python manage.py makemigrations
python manage.py migrate
python seed.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

- Check troubleshooting section
- Create an issue in the repository
- Contact the development team

## Future Enhancements

- Payment gateway integration
- Email notifications
- SMS alerts
- Advanced filtering options
- Mobile application
- Multi-language support