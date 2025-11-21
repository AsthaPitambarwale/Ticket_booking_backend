🎬 Movie Ticket Booking System – Backend (Django + DRF + JWT)

🚀 Fully Production-Grade | Concurrency Safe | Swagger Enabled | Custom HTML Landing Page

This project is a fully-featured Movie Ticket Booking Backend System built with:

•   Django
•   Django REST Framework
•   JWT Authentication
•   HTML + CSS Landing Page
•   Swagger API Documentation
•   SQLite (default) / PostgreSQL (optional for concurrency tests)
•   Concurrency-safe seat booking
•   Unit tests (including concurrent booking simulation)

This backend implements a reliable, scalable, and secure movie ticket booking workflow with real-world booking constraints, race-condition safe seat booking.
________________________________________
📌 Features Overview

🔐 Authentication (JWT)
•   User Signup
•   Login → Access/Refresh Token
•   Secured endpoints using Bearer Token

🎥 Movie & Show Management
•   List all movies
•   List all shows for each movie
•   Automatic available seat calculation

🎟️ Booking System
•   Seat booking with:
o   Database row locking (select_for_update)
o   Retry logic with exponential backoff
o   Double-booking protection (DB + logic)
o   Capacity validation
•   Seat cancellation
•   User-only booking cancellation (authorization enforced)
•   View all bookings of logged-in user

📄 API Documentation
•   Interactive Swagger Docs
•   Token authentication supported
•   Example inputs & outputs included

🧪 Unit Tests
Includes tests for:
•   Booking
•   Cancellation
•   Permission checks
•   Concurrency simulation using threads

🛠️ Bonus Improvements
•   Input validation using DRF serializer rules
•   Unique DB constraints on seat booking
•   Sample data generator
•   Dockerfile + optional docker-compose
•   Clean modular code & custom permissions
________________________________________
🏗️ Tech Stack

Component   = Technology
Backend  =  Django 4+
API Layer = Django REST Framework
Authentication = JWT (djangorestframework-simplejwt)
Documentation = Swagger (drf-yasg)
Database = PostgreSQL (recommended)
Testing = Django TestCase + PyTest (optional)
UI  =  Custom HTML + CSS landing page
________________________________________

📁 Project Structure

movie_booking/
│
├── movie_booking/         # Core project
│   ├── settings.py
│   ├── urls.py
│   └── templates/
│        └── landing.html 
├── api/                   # Main application
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   |── tests.py
│   └── management/
│       └── commands/
│           └── createsampledata.py
│       
├── requirements.txt
├── Dockerfile
└── README.md  <-- this file
________________________________________
⚙️ Setup Instructions

1️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Database(optional)
 (Recommended: Add PostgreSQL - only for concurrent booking testing)

In settings.py: 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ' your-table-name ',(e.g. moviedb)
        'USER': ' your-username',(e.g. pguser)
        'PASSWORD': ' your-password',(e.g. pgpass)
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Admin User
python manage.py createsuperuser

6️⃣ Generate Sample Data
python manage.py createsampledata
This creates:
•   A demo user: username: demo | password: demopass
•   2 movies and 3 shows

7️⃣ Start the Server
python manage.py runserver
________________________________________
🖥️ ✨ New Feature: HTML Landing Page

This project includes a beautiful, responsive, modern HTML homepage instead of the default Django 404 page.

📌 Purpose of the HTML Landing Page
•	Creates a professional first impression for evaluators
•	Provides quick access buttons to:
o	Swagger API Documentation
o	Movies API
o	Admin Panel
•	Displays API overview and project description
•	Shows essential endpoints
•	Makes the project presentable and standout in interviews

📁 Landing Page File Location:
movie_booking/templates/landing.html

🌐 URL:
http://127.0.0.1:8000/

🎨 Technologies used:
•	HTML5
•	Custom CSS
•	Glassmorphism UI
•	Responsive layout
•	Modern button animations

This makes your project look polished and premium quality.
________________________________________
🔑 JWT Authentication

Login → Get Tokens
POST /api/login/
{
  "username": "demo",
  "password": "demopass"
}
Response
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}

Use in Headers
Authorization: Bearer <access_token>
________________________________________
📚 API Endpoints

🧑 Auth
Method  Endpoint    Description
POST    /api/signup/    User Registration
POST    /api/login/ JWT Login
________________________________________
🎬 Movies & Shows
Method  Endpoint    Description
GET /api/movies/    List all movies
GET /api/movies/<id>/shows/ Shows for a movie
________________________________________
🎟️ Bookings
Method  Endpoint    Auth    Description
POST    /api/shows/<id>/book/   🔒 Yes  Book a seat
POST    /api/bookings/<id>/cancel/  🔒 Yes  Cancel your booking
GET /api/my-bookings/   🔒 Yes  Your booking history
________________________________________
🧠 Concurrency-Safe Booking Logic
This system handles multiple users trying to book the same seat simultaneously using:
✔ select_for_update()
Locks the row to guarantee seat availability checking is safe.
✔ Unique DB constraint
unique_together = ('show', 'seat_number')
✔ Retry mechanism
Automatically retries the booking with:
•   exponential backoff
•   random jitter (prevents thundering herd)
✔ Correct HTTP responses
•   201 → Seat booked
•   409 → Already booked / show full
•   500 → Too much contention
This is production-grade engineering.
________________________________________
📄 Swagger Documentation

Visit:
👉 /swagger/
Features:
•   Full schema
•   Try-out mode
•   JWT Bearer Authentication
•   Example bodies
•   Auto-generated models
________________________________________
🧪 Running Tests

python manage.py test
Tests include:
✔ Booking
✔ Cancellation
✔ Preventing other users from cancelling
✔ Concurrency simulation using threads
________________________________________
🐳 Docker Support (Optional)

Build:
docker build -t movie-backend .
Run:
docker run -p 8000:8000 movie-backend
You can also add docker-compose with PostgreSQL (optional).
________________________________________
🎭 Demo Credentials

After running:
python manage.py createsampledata
Use:
Key Value
username    demo
password    demopass
________________________________________
🏁 Conclusion

This backend system exceeds typical assignment expectations by implementing:
✨ HTML landing page (modern, animated, beautiful)
✨ production-level booking logic
✨ database locking
✨ concurrency-safe algorithms
✨ automated tests
✨ Swagger with JWT support
✨ clean architecture and validation
✨ Docker deployment option

It is ready for real world usage, scalability, and professional demonstration.


