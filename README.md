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

- **Backend**: Django 5.2.4, Django REST Framework
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
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install python-dotenv
pip install mysqlclient
```

### 4. MySQL Database Setup

#### Option A: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create a new schema:
   ```sql
   CREATE SCHEMA travelbooking;
   ```
4. Note down your MySQL credentials (username, password, host, port)

#### Option B: Using Command Line

```bash
mysql -u root -p
CREATE DATABASE travelbooking;
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON travelbooking.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Environment Configuration

Create a `.env` file in the root directory and add:

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
- `POST /api/register/`
- `POST /api/login/`
- `POST /api/logout/`
- `GET/PUT /api/profile/`
- `POST /api/token/`
- `POST /api/token/refresh/`

### Travel Options
- `GET /api/travel-options/`
- `POST /api/travel-options/`
- `GET /api/travel-options/{id}/`
- `GET /api/travel-search/`

### Bookings
- `GET /api/bookings/`
- `POST /api/bookings/`
- `GET /api/bookings/{id}/`
- `POST /api/bookings/{id}/cancel/`

### Search Parameters
- `type`: flight, train, bus
- `source`: departure city
- `destination`: arrival city
- `date_from` & `date_to`: date range
- `min_price` & `max_price`: price range

## Usage Examples

### Creating a Booking (API)

```json
POST /api/bookings/
{
    "travel_option": 1,
    "number_of_seats": 2,
    "passenger_details": [
        {
            "name": "John Doe",
            "age": 30,
            "id_number": "ID123456",
            "special_requirements": "None"
        },
        {
            "name": "Jane Doe",
            "age": 28,
            "id_number": "ID789012",
            "special_requirements": "Vegetarian meal"
        }
    ]
}
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
├── templates/
├── static/
├── seed.py
├── manage.py
└── requirements.txt
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Verify MySQL is running
   - Check credentials in `.env`
   - Ensure database exists

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