# 🎬 Movie Ticket Booking System – Backend

### **Django + DRF + JWT | Concurrency Safe | Swagger Enabled**

A fully production-ready backend system with safe seat booking, JWT authentication, Swagger documentation, and a professional HTML landing page.

---

## 📌 Features

### 🔐 Authentication (JWT)

* User Signup
* Login → Access + Refresh Tokens
* Secured endpoints using Bearer Token

### 🎥 Movies & Shows

* List movies
* List shows for movies
* Automatic seat calculation

### 🎟️ Booking System

* Concurrency-safe seat booking
* Prevents double booking
* `select_for_update` row locking
* Retry logic with exponential backoff
* Seat cancellation (only by booking owner)
* View user bookings

### 📄 API Documentation

* Swagger UI
* Try Out requests
* JWT Authentication support

### 🧪 Unit Tests

* Booking tests
* Cancellation tests
* Permission tests
* Concurrency simulation

---

## 🏗️ Tech Stack

| Component | Technology              |
| --------- | ----------------------- |
| Backend   | Django 4+               |
| API Layer | Django REST Framework   |
| Auth      | JWT (SimpleJWT)         |
| Docs      | Swagger (drf-yasg)      |
| Database  | SQLite / PostgreSQL     |
| UI        | HTML + CSS Landing Page |

---

## 📁 Project Structure

```text
movie_booking/
│
├── movie_booking/                # Core project
│   ├── settings.py
│   ├── urls.py
│   └── templates/
│       └── landing.html
│
├── api/                          # Main application
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           └── createsampledata.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ (Optional) Configure PostgreSQL

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "moviedb",
        "USER": "pguser",
        "PASSWORD": "pgpass",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

### 6️⃣ Generate Sample Data

```bash
python manage.py createsampledata
```

### 7️⃣ Start Server

```bash
python manage.py runserver
```

---

## 🖥️ HTML Landing Page

A modern, animated landing page is included.

**Path:**

```
movie_booking/templates/landing.html
```

**URL:**

```
http://127.0.0.1:8000/
```

Features:

* Glassmorphism UI
* Responsive design
* Links to Swagger, Admin Panel & APIs

---

## 🔑 JWT Authentication

### Login

```http
POST /api/login/
```

Request:

```json
{
  "username": "demo",
  "password": "demopass"
}
```

Response:

```json
{
  "refresh": "token_here",
  "access": "token_here"
}
```

Use in requests:

```
Authorization: Bearer <access_token>
```

---

## 📚 API Endpoints

### 🧑 Authentication

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | `/api/signup/` | User registration |
| POST   | `/api/login/`  | JWT login         |

---

### 🎬 Movies & Shows

| Method | Endpoint                  | Description       |
| ------ | ------------------------- | ----------------- |
| GET    | `/api/movies/`            | List all movies   |
| GET    | `/api/movies/<id>/shows/` | Shows for a movie |

---

### 🎟️ Bookings

| Method | Endpoint                     | Auth   | Description     |
| ------ | ---------------------------- | ------ | --------------- |
| POST   | `/api/shows/<id>/book/`      | 🔒 Yes | Book a seat     |
| POST   | `/api/bookings/<id>/cancel/` | 🔒 Yes | Cancel booking  |
| GET    | `/api/my-bookings/`          | 🔒 Yes | User's bookings |

---

## 🧠 Concurrency-Safe Booking Logic

Handles simultaneous seat booking using:

### ✔ Row-level locking

`select_for_update()` ensures one seat is booked only once.

### ✔ Unique constraint

```python
unique_together = ("show", "seat_number")
```

### ✔ Retry logic

With exponential backoff + random jitter.

### ✔ Correct status codes

* `201` Seat booked
* `409` Already booked / full
* `500` High contention

---

## 📄 Swagger API Docs

URL:

```
/swagger/
```

Features:

* Interactive API testing
* JWT auth
* Model schemas

---

## 🧪 Running Tests

```bash
python manage.py test
```

Tests:

* Booking
* Cancellation
* Concurrent booking

---

## 🐳 Docker Support

### Build

```bash
docker build -t movie-backend .
```

### Run

```bash
docker run -p 8000:8000 movie-backend
```

---

## 🎭 Demo Credentials

| Username | Password |
| -------- | -------- |
| demo     | demopass |

---

## 🏁 Conclusion

This backend delivers:

* ✔ Production-level booking system
* ✔ Concurrency-safe logic
* ✔ Swagger documentation
* ✔ JWT authentication
* ✔ HTML landing page
* ✔ Docker support
* ✔ Clean modular architecture


It is ready for real world usage, scalability, and professional demonstration.

